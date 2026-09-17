from pathlib import Path
from tempfile import TemporaryDirectory

from pet_brain.speech import SpeechConfig, WhisperSpeech


def test_speech_config_defaults() -> None:
    config = SpeechConfig()
    assert config.model == "base"
    assert config.sample_rate == 16_000


def test_record_rejects_non_positive_duration() -> None:
    speech = WhisperSpeech()
    for seconds in (0, -1):
        try:
            speech.record(seconds)
        except ValueError as exc:
            assert "positive" in str(exc)
        else:
            raise AssertionError("record should reject non-positive duration")


def test_transcribe_uses_loaded_model_and_cleans_path() -> None:
    class FakeModel:
        def transcribe(self, path: str, **kwargs):
            assert Path(path).exists()
            return {"text": " hello pet "}

    speech = WhisperSpeech()
    speech._model = FakeModel()
    with TemporaryDirectory() as directory:
        path = Path(directory) / "sample.wav"
        path.write_bytes(b"wav")
        assert speech.transcribe(path) == "hello pet"
