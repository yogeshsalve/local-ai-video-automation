import whisper
from pathlib import Path


# --------------------------------------------------
# Configuration
# --------------------------------------------------

AUDIO_FILE = Path("assets/audio/generated/day3_narration.wav")
OUTPUT_DIR = Path("assets/audio/generated")
MODEL_NAME = "tiny.en"


# --------------------------------------------------
# Helper: Convert seconds to SRT timestamp
# --------------------------------------------------

def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int(round((seconds - int(seconds)) * 1000))

    # Handle 1000 milliseconds
    if milliseconds == 1000:
        secs += 1
        milliseconds = 0

    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"


# --------------------------------------------------
# Main transcription function
# --------------------------------------------------

def main():

    # Check input audio
    if not AUDIO_FILE.exists():
        raise FileNotFoundError(
            f"Audio file not found: {AUDIO_FILE}"
        )

    # Create output directory if needed
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Output SRT file
    srt_file = OUTPUT_DIR / "day4_transcription.srt"

    print("=" * 50)
    print("LOCAL AI VIDEO AUTOMATION")
    print("Whisper Audio Transcription")
    print("=" * 50)

    print(f"Audio file : {AUDIO_FILE}")
    print(f"Model      : {MODEL_NAME}")
    print()

    # Load Whisper model
    print("Loading Whisper model...")
    model = whisper.load_model(MODEL_NAME)

    print("Model loaded successfully.")
    print()

    # Transcribe audio
    print("Transcribing audio...")

    result = model.transcribe(
        str(AUDIO_FILE),
        language="en",
        task="transcribe",
        fp16=False,
    )

    print("Transcription completed.")
    print()

    # Create SRT
    print("Creating SRT file...")

    with open(srt_file, "w", encoding="utf-8") as file:

        for index, segment in enumerate(
            result["segments"],
            start=1
        ):

            start = segment["start"]
            end = segment["end"]
            text = segment["text"].strip()

            file.write(f"{index}\n")

            file.write(
                f"{format_timestamp(start)} --> "
                f"{format_timestamp(end)}\n"
            )

            file.write(f"{text}\n\n")

    print(f"SRT created successfully:")
    print(srt_file)
    print()

    print("=" * 50)
    print("TRANSCRIPTION PIPELINE COMPLETED")
    print("=" * 50)


# --------------------------------------------------
# Program entry point
# --------------------------------------------------

if __name__ == "__main__":
    main()