from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile


@dataclass(frozen=True)
class SpeechConfig:
    model: str = "base"
    language: str | None = None
    sample_rate: int = 16_000


class WhisperSpeech:
    """Local microphone recorder and Whisper transcriber for the Mac brain."""

    def __init__(self, config: SpeechConfig | None = None) -> None:
        self.config = config or SpeechConfig()
        self._model = None

    def _load_model(self):
        if self._model is None:
            import whisper

            self._model = whisper.load_model(self.config.model)
        return self._model

    def record(self, seconds: float = 5.0) -> Path:
        if seconds <= 0:
            raise ValueError("seconds must be positive")

        import sounddevice as sd
        from scipy.io.wavfile import write

        frames = int(seconds * self.config.sample_rate)
        audio = sd.rec(frames, samplerate=self.config.sample_rate, channels=1, dtype="int16")
        sd.wait()

        handle = NamedTemporaryFile(suffix=".wav", delete=False)
        path = Path(handle.name)
        handle.close()
        write(path, self.config.sample_rate, audio)
        return path

    def transcribe(self, audio_path: str | Path) -> str:
        model = self._load_model()
        options = {}
        if self.config.language:
            options["language"] = self.config.language
        result = model.transcribe(str(audio_path), fp16=False, **options)
        return result.get("text", "").strip()

    def listen_once(self, seconds: float = 5.0) -> str:
        path = self.record(seconds)
        try:
            return self.transcribe(path)
        finally:
            path.unlink(missing_ok=True)
