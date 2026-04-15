# 🎵 Source Separation

## 🔗 Navegação

**[🏠 AslamSys](https://github.com/AslamSys)** → **[📚 _system](https://github.com/AslamSys/_system)** → **[📂 Aslam (Orange Pi 5 16GB)](https://github.com/AslamSys/_system/blob/main/hardware/mordomo%20-%20(orange-pi-5-16gb)/README.md)** → **mordomo-source-separation**

### Containers Relacionados (aslam)
- [mordomo-audio-bridge](https://github.com/AslamSys/mordomo-audio-bridge)
- [mordomo-audio-capture-vad](https://github.com/AslamSys/mordomo-audio-capture-vad)
- [mordomo-wake-word-detector](https://github.com/AslamSys/mordomo-wake-word-detector)
- [mordomo-speaker-verification](https://github.com/AslamSys/mordomo-speaker-verification)
- [mordomo-whisper-asr](https://github.com/AslamSys/mordomo-whisper-asr)
- [mordomo-speaker-id-diarization](https://github.com/AslamSys/mordomo-speaker-id-diarization)
- [mordomo-core-gateway](https://github.com/AslamSys/mordomo-core-gateway)
- [mordomo-orchestrator](https://github.com/AslamSys/mordomo-orchestrator)
- [mordomo-brain](https://github.com/AslamSys/mordomo-brain)
- [mordomo-tts-engine](https://github.com/AslamSys/mordomo-tts-engine)
- [mordomo-system-watchdog](https://github.com/AslamSys/mordomo-system-watchdog)
- [mordomo-openclaw-agent](https://github.com/AslamSys/mordomo-openclaw-agent)

---

**Container:** `source-separation`  
**Ecossistema:** Mordomo  
**Posição no Fluxo:** Opcional/Condicional - separação de vozes

---

## 📋 Propósito

Separar vozes sobrepostas quando duas pessoas falam simultaneamente, melhorando precisão do STT e Speaker ID.

---

## 🎯 Responsabilidades

- ✅ Ativado APENAS quando Speaker ID detecta overlap
- ✅ Separar áudio em canais por falante
- ✅ Reenviar áudio separado para STT refinado
- ✅ Não afetar latência em conversas normais

---

## 🔧 Tecnologias

**Linguagem:** Python (obrigatório - PyTorch)

**Principal:** Demucs
- Separação de sources (vozes, música, etc)
- Versão lightweight para ARM
- **Backend:** PyTorch (C++ libtorch nativo)

**Modelo:** `htdemucs_ft` (fine-tuned para voz)

**Performance:** Model inference em PyTorch C++, processamento intensivo de CPU. Python overhead desprezível (<1% do total 1-3s).

---

## 📊 Especificações

```yaml
Input:
  Audio com overlap
  Duration: 1-5 segundos
  Sample Rate: 16000 Hz

Separation:
  Sources: 2-3 vozes
  Quality: Alta
  
Performance:
  CPU: 60-80% spike (intensivo!)
  RAM: ~ 1.5 GB
  Latency: 1-3 segundos
  Uso: < 5% do tempo (apenas quando overlap)
```

---

## 🔌 Interfaces

### Input (NATS)
```python
# Enviado por: Speaker ID quando detecta overlap_detected=true

## 🔗 Navegação

**[🏠 AslamSys](https://github.com/AslamSys)** → **[📚 _system](https://github.com/AslamSys/_system)** → **[📂 Aslam (Orange Pi 5 16GB)](https://github.com/AslamSys/_system/blob/main/hardware/mordomo%20-%20(orange-pi-5-16gb)/README.md)** → **mordomo-source-separation**

### Containers Relacionados (aslam)
- [mordomo-audio-bridge](https://github.com/AslamSys/mordomo-audio-bridge)
- [mordomo-audio-capture-vad](https://github.com/AslamSys/mordomo-audio-capture-vad)
- [mordomo-wake-word-detector](https://github.com/AslamSys/mordomo-wake-word-detector)
- [mordomo-speaker-verification](https://github.com/AslamSys/mordomo-speaker-verification)
- [mordomo-whisper-asr](https://github.com/AslamSys/mordomo-whisper-asr)
- [mordomo-speaker-id-diarization](https://github.com/AslamSys/mordomo-speaker-id-diarization)
- [mordomo-core-gateway](https://github.com/AslamSys/mordomo-core-gateway)
- [mordomo-orchestrator](https://github.com/AslamSys/mordomo-orchestrator)
- [mordomo-brain](https://github.com/AslamSys/mordomo-brain)
- [mordomo-tts-engine](https://github.com/AslamSys/mordomo-tts-engine)
- [mordomo-system-watchdog](https://github.com/AslamSys/mordomo-system-watchdog)
- [mordomo-openclaw-agent](https://github.com/AslamSys/mordomo-openclaw-agent)

---
subject: "audio.overlap_detected"
payload: {
  "audio": "<base64 encoded PCM>",
  "duration": 2.5,
  "speakers": ["user_1", "user_2"],
  "conversation_id": "uuid",
  "timestamp": 1732723200.123
}
```

### Output (NATS)
```python
# Envia áudio separado de volta para Whisper reprocessar

## 🔗 Navegação

**[🏠 AslamSys](https://github.com/AslamSys)** → **[📚 _system](https://github.com/AslamSys/_system)** → **[📂 Aslam (Orange Pi 5 16GB)](https://github.com/AslamSys/_system/blob/main/hardware/mordomo%20-%20(orange-pi-5-16gb)/README.md)** → **mordomo-source-separation**

### Containers Relacionados (aslam)
- [mordomo-audio-bridge](https://github.com/AslamSys/mordomo-audio-bridge)
- [mordomo-audio-capture-vad](https://github.com/AslamSys/mordomo-audio-capture-vad)
- [mordomo-wake-word-detector](https://github.com/AslamSys/mordomo-wake-word-detector)
- [mordomo-speaker-verification](https://github.com/AslamSys/mordomo-speaker-verification)
- [mordomo-whisper-asr](https://github.com/AslamSys/mordomo-whisper-asr)
- [mordomo-speaker-id-diarization](https://github.com/AslamSys/mordomo-speaker-id-diarization)
- [mordomo-core-gateway](https://github.com/AslamSys/mordomo-core-gateway)
- [mordomo-orchestrator](https://github.com/AslamSys/mordomo-orchestrator)
- [mordomo-brain](https://github.com/AslamSys/mordomo-brain)
- [mordomo-tts-engine](https://github.com/AslamSys/mordomo-tts-engine)
- [mordomo-system-watchdog](https://github.com/AslamSys/mordomo-system-watchdog)
- [mordomo-openclaw-agent](https://github.com/AslamSys/mordomo-openclaw-agent)

---
subject: "audio.separated"
payload: {
  "channels": [
    {
      "audio": "<base64 PCM channel 1>",
      "speaker_id": "user_1",
      "confidence": 0.85
    },
    {
      "audio": "<base64 PCM channel 2>",
      "speaker_id": "user_2",
      "confidence": 0.78
    }
  ],
  "conversation_id": "uuid",
  "original_duration": 2.5,
  "timestamp": 1732723201.456
}

# Whisper ASR subscreve audio.separated e retranscribe

## 🔗 Navegação

**[🏠 AslamSys](https://github.com/AslamSys)** → **[📚 _system](https://github.com/AslamSys/_system)** → **[📂 Aslam (Orange Pi 5 16GB)](https://github.com/AslamSys/_system/blob/main/hardware/mordomo%20-%20(orange-pi-5-16gb)/README.md)** → **mordomo-source-separation**

### Containers Relacionados (aslam)
- [mordomo-audio-bridge](https://github.com/AslamSys/mordomo-audio-bridge)
- [mordomo-audio-capture-vad](https://github.com/AslamSys/mordomo-audio-capture-vad)
- [mordomo-wake-word-detector](https://github.com/AslamSys/mordomo-wake-word-detector)
- [mordomo-speaker-verification](https://github.com/AslamSys/mordomo-speaker-verification)
- [mordomo-whisper-asr](https://github.com/AslamSys/mordomo-whisper-asr)
- [mordomo-speaker-id-diarization](https://github.com/AslamSys/mordomo-speaker-id-diarization)
- [mordomo-core-gateway](https://github.com/AslamSys/mordomo-core-gateway)
- [mordomo-orchestrator](https://github.com/AslamSys/mordomo-orchestrator)
- [mordomo-brain](https://github.com/AslamSys/mordomo-brain)
- [mordomo-tts-engine](https://github.com/AslamSys/mordomo-tts-engine)
- [mordomo-system-watchdog](https://github.com/AslamSys/mordomo-system-watchdog)
- [mordomo-openclaw-agent](https://github.com/AslamSys/mordomo-openclaw-agent)

---
# Nova transcrição → Speaker ID → speech.diarized (com overlap resolvido)

## 🔗 Navegação

**[🏠 AslamSys](https://github.com/AslamSys)** → **[📚 _system](https://github.com/AslamSys/_system)** → **[📂 Aslam (Orange Pi 5 16GB)](https://github.com/AslamSys/_system/blob/main/hardware/mordomo%20-%20(orange-pi-5-16gb)/README.md)** → **mordomo-source-separation**

### Containers Relacionados (aslam)
- [mordomo-audio-bridge](https://github.com/AslamSys/mordomo-audio-bridge)
- [mordomo-audio-capture-vad](https://github.com/AslamSys/mordomo-audio-capture-vad)
- [mordomo-wake-word-detector](https://github.com/AslamSys/mordomo-wake-word-detector)
- [mordomo-speaker-verification](https://github.com/AslamSys/mordomo-speaker-verification)
- [mordomo-whisper-asr](https://github.com/AslamSys/mordomo-whisper-asr)
- [mordomo-speaker-id-diarization](https://github.com/AslamSys/mordomo-speaker-id-diarization)
- [mordomo-core-gateway](https://github.com/AslamSys/mordomo-core-gateway)
- [mordomo-orchestrator](https://github.com/AslamSys/mordomo-orchestrator)
- [mordomo-brain](https://github.com/AslamSys/mordomo-brain)
- [mordomo-tts-engine](https://github.com/AslamSys/mordomo-tts-engine)
- [mordomo-system-watchdog](https://github.com/AslamSys/mordomo-system-watchdog)
- [mordomo-openclaw-agent](https://github.com/AslamSys/mordomo-openclaw-agent)

---
```

---

## ⚙️ Configuração

```yaml
demucs:
  model: "htdemucs_ft"
  device: "cpu"
  shifts: 1
  overlap: 0.25
  
processing:
  max_duration: 5.0  # segundos
  batch_size: 1
  num_workers: 2
  
trigger:
  min_overlap_duration: 0.5
  confidence_threshold: 0.6
```

---

## 📈 Métricas

```python
source_separation_requests_total
source_separation_latency_seconds
source_separation_success_total
source_separation_quality_score
```

---

## 🔗 Integração

### Fluxo Completo de Overlap

```
1. Whisper transcribe → Speaker ID (áudio + texto)
   ↓
2. Speaker ID detecta overlap (2+ vozes simultâneas)
   └─ NATS: audio.overlap_detected
   ↓
3. Source Separation recebe e processa (1-3s)
   └─ Demucs separa em canais (channel 1, channel 2)
   ↓
4. Source Separation publica: NATS audio.separated
   ↓
5. Whisper subscreve audio.separated
   └─ Retranscribe cada canal separadamente
   ↓
6. Whisper → Speaker ID (nova transcrição refinada)
   └─ Agora sem overlap, identifica corretamente
   ↓
7. Speaker ID → NATS: speech.diarized (overlap resolvido)
```

**Recebe de:** Speaker ID (NATS `audio.overlap_detected`)  
**Envia para:** Whisper ASR (NATS `audio.separated`)  
**Monitora:** Prometheus

---

**⚠️ Nota:** Container pesado (60-80% CPU, 1.5GB RAM) - usar apenas quando necessário (<5% do tempo)

---

**Versão:** 1.0
