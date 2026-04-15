import os
from dataclasses import dataclass, field


@dataclass
class Config:
    # NATS
    nats_url: str = field(default_factory=lambda: os.getenv("NATS_URL", "nats://nats:4222"))

    # Demucs model — htdemucs_ft is fine-tuned for vocals/voice separation
    demucs_model: str = field(default_factory=lambda: os.getenv("DEMUCS_MODEL", "htdemucs_ft"))

    # Audio
    sample_rate: int = 44100  # Demucs native rate; will resample input from 16kHz

    # Max audio duration accepted (seconds) — guard against huge payloads
    max_duration_seconds: float = field(
        default_factory=lambda: float(os.getenv("MAX_DURATION_SECONDS", "10.0"))
    )

    # Number of sources to separate (2 = vocals + background, or 2 speakers)
    num_sources: int = field(default_factory=lambda: int(os.getenv("NUM_SOURCES", "2")))

    # Device: "cpu" always on Orange Pi (no CUDA)
    device: str = field(default_factory=lambda: os.getenv("DEMUCS_DEVICE", "cpu"))


config = Config()
