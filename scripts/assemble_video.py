import subprocess
from pathlib import Path


# --------------------------------------------------
# Configuration
# --------------------------------------------------

AUDIO_FILE = Path("assets/audio/generated/day3_narration.wav")
SRT_FILE = Path("assets/audio/generated/day4_transcription.srt")

OUTPUT_DIR = Path("output")
OUTPUT_FILE = OUTPUT_DIR / "day5_visual_video_v2.mp4"
WIDTH = 1920
HEIGHT = 1080
FPS = 30


# --------------------------------------------------
# Check required files
# --------------------------------------------------

def check_files():

    if not AUDIO_FILE.exists():
        raise FileNotFoundError(
            f"Audio file not found: {AUDIO_FILE}"
        )

    if not SRT_FILE.exists():
        raise FileNotFoundError(
            f"SRT file not found: {SRT_FILE}"
        )


# --------------------------------------------------
# Prepare Windows path for FFmpeg subtitles filter
# --------------------------------------------------

def prepare_subtitle_path():

    subtitle_path = SRT_FILE.resolve()

    # Convert Windows backslashes to forward slashes
    subtitle_path = str(subtitle_path).replace("\\", "/")

    # Escape Windows drive-letter colon for FFmpeg filter syntax
    subtitle_path = subtitle_path.replace(":", r"\:")

    return subtitle_path


# --------------------------------------------------
# Create video
# --------------------------------------------------

def create_video():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    subtitle_path = prepare_subtitle_path()

    output_path = OUTPUT_FILE.resolve()

    print("=" * 50)
    print("LOCAL AI VIDEO AUTOMATION")
    print("Day 5 - Video Assembly")
    print("=" * 50)

    print(f"Audio : {AUDIO_FILE.resolve()}")
    print(f"SRT   : {SRT_FILE.resolve()}")
    print(f"Output: {output_path}")
    print()

    command = [
        "ffmpeg",
        "-y",

     	 # Background image
      	"-loop",
	"1",

	"-i",
	str(Path("assets/images/generated/day5_fabric_background.png").resolve()),

	# Narration
	"-i",
	str(AUDIO_FILE.resolve()),

        # Burn subtitles
        "-vf",
        f"subtitles='{subtitle_path}'",

        # Video encoding
       	"-c:v",
	"libx264",

	"-preset",
	"veryfast",

	"-crf",
	"23",

	"-pix_fmt",
	"yuv420p",

        # Audio encoding
        "-c:a",
        "aac",

        "-b:a",
        "192k",

        # Stop when audio ends
        "-shortest",

        str(output_path),
    ]

    print("Running FFmpeg...")
    print()

    subprocess.run(
        command,
        check=True
    )

    print()
    print("=" * 50)
    print("VIDEO CREATED SUCCESSFULLY")
    print("=" * 50)
    print(f"Output: {output_path}")


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    check_files()
    create_video()


if __name__ == "__main__":
    main()