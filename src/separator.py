"""
Demucs-based voice source separator.

Receives a mixed PCM audio clip (int16, 16kHz, mono) encoded as base64,
separates into individual voice channels, returns them as base64 PCM arrays
resampled back to 16kHz.
"""
import base64
import logging
from typing import Optional

import numpy as np
import torch
import torchaudio
from demucs.apply import apply_model
from demucs.pretrained import get_model

logger = logging.getLogger("source-separation.separator")


class SourceSeparator:
    def __init__(self, model_name: str, device: str, output_sample_rate: int = 16000):
        self._device = torch.device(device)
        self._output_sample_rate = output_sample_rate

        logger.info(f"Loading Demucs model '{model_name}' on {device}…")
        self._model = get_model(model_name)
        self._model.to(self._device)
        self._model.eval()
        self._model_rate = self._model.samplerate  # typically 44100
        logger.info(f"Demucs ready (model_rate={self._model_rate}Hz, sources={self._model.sources})")

    def separate(self, pcm_bytes: bytes, input_sample_rate: int = 16000) -> list[bytes]:
        """
        Separate mixed PCM (int16) into source channels.

        Returns a list of raw PCM bytes (int16, 16kHz, mono), one per source.
        """
        # Decode int16 → float32 normalised [-1, 1]
        samples = np.frombuffer(pcm_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        audio = torch.from_numpy(samples).unsqueeze(0)  # (1, T)

        # Resample to model rate
        if input_sample_rate != self._model_rate:
            audio = torchaudio.functional.resample(audio, input_sample_rate, self._model_rate)

        # Demucs expects (batch, channels, time) — stereo preferred, duplicate mono
        audio_stereo = audio.repeat(2, 1).unsqueeze(0).to(self._device)  # (1, 2, T)

        with torch.no_grad():
            separated = apply_model(self._model, audio_stereo, device=self._device)
        # separated shape: (batch=1, sources, channels=2, T)

        results = []
        for src_idx in range(separated.shape[1]):
            src = separated[0, src_idx]  # (2, T) stereo
            src_mono = src.mean(dim=0, keepdim=True)  # (1, T)

            # Resample back to 16kHz
            if self._model_rate != self._output_sample_rate:
                src_mono = torchaudio.functional.resample(
                    src_mono, self._model_rate, self._output_sample_rate
                )

            # Convert to int16 PCM
            pcm = (src_mono.squeeze(0).cpu().numpy() * 32768.0).clip(-32768, 32767).astype(np.int16)
            results.append(pcm.tobytes())

        return results
