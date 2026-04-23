"""
Main entry point — source separation service.

SUB: mordomo.audio.overlap_detected
PUB: reply channel (request/reply)
"""
import asyncio
import base64
import json
import logging
import time

import nats

from src.config import config
from src.separator import SourceSeparator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger("source-separation")

_separator: SourceSeparator | None = None


async def _handle_overlap(msg):
    try:
        data = json.loads(msg.data.decode())
    except Exception as e:
        logger.error(f"Invalid payload: {e}")
        return

    audio_b64 = data.get("audio")
    conversation_id = data.get("conversation_id", "")
    speakers = data.get("speakers", [])
    original_duration = data.get("duration", 0.0)

    if not audio_b64:
        logger.warning("Received overlap_detected with no audio field — ignoring")
        return

    if original_duration > config.max_duration_seconds:
        logger.warning(
            f"Audio too long ({original_duration}s > {config.max_duration_seconds}s) — ignoring"
        )
        return

    logger.info(f"Separating audio [{conversation_id}] duration={original_duration}s speakers={speakers}")
    t0 = time.monotonic()

    try:
        pcm_bytes = base64.b64decode(audio_b64)
        channels = _separator.separate(pcm_bytes, input_sample_rate=16000)
    except Exception as e:
        logger.error(f"Separation failed: {e}")
        return

    elapsed = time.monotonic() - t0
    logger.info(f"Separation done in {elapsed:.2f}s — {len(channels)} sources")

    channel_payloads = []
    for i, ch_pcm in enumerate(channels):
        channel_payloads.append({
            "audio": base64.b64encode(ch_pcm).decode(),
            "speaker_id": speakers[i] if i < len(speakers) else f"source_{i}",
            "confidence": 1.0,  # Demucs doesn't produce per-source confidence scores
        })

    result = {
        "channels": channel_payloads,
        "conversation_id": conversation_id,
        "original_duration": original_duration,
        "separation_time_seconds": round(elapsed, 3),
        "timestamp": time.time(),
    }

    await msg.respond(json.dumps(result).encode())


async def main():
    global _separator

    logger.info("Loading Demucs model…")
    _separator = SourceSeparator(
        model_name=config.demucs_model,
        device=config.device,
    )

    async def error_cb(e): logger.error(f"NATS error: {e}")
    async def reconnected_cb(): logger.warning("NATS reconnected")
    async def disconnected_cb(): logger.warning("NATS disconnected")

    nc = await nats.connect(
        config.nats_url,
        error_cb=error_cb,
        reconnected_cb=reconnected_cb,
        disconnected_cb=disconnected_cb,
    )
    logger.info(f"Connected to NATS: {config.nats_url}")

    await nc.subscribe("mordomo.audio.overlap_detected", cb=_handle_overlap)
    logger.info("Subscribed to mordomo.audio.overlap_detected — waiting for overlap events")

    try:
        await asyncio.Event().wait()
    except (asyncio.CancelledError, KeyboardInterrupt):
        pass
    finally:
        await nc.drain()
        logger.info("Shutdown complete.")


if __name__ == "__main__":
    asyncio.run(main())
