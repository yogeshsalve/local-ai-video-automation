import json
import subprocess
from pathlib import Path


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CONFIG_FILE = PROJECT_ROOT / "config" / "video_config.json"


# --------------------------------------------------
# Load configuration
# --------------------------------------------------

def load_config():

    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {CONFIG_FILE}"
        )

    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# --------------------------------------------------
# Resolve project-relative path
# --------------------------------------------------

def resolve_project_path(path_string):

    path = Path(path_string)

    if path.is_absolute():
        return path

    return PROJECT_ROOT / path


# --------------------------------------------------
# Prepare subtitle path for FFmpeg
# --------------------------------------------------

def prepare_subtitle_path(srt_file):

    subtitle_path = srt_file.resolve()

    # Convert Windows backslashes to forward slashes
    subtitle_path = str(
        subtitle_path
    ).replace("\\", "/")

    # Escape drive-letter colon for FFmpeg filter syntax
    subtitle_path = subtitle_path.replace(
        ":",
        r"\:"
    )

    return subtitle_path


# --------------------------------------------------
# Validate required files
# --------------------------------------------------

def check_files(audio_file, srt_file, background_file):

    required_files = [
        audio_file,
        srt_file,
        background_file,
    ]

    for file_path in required_files:

        if not file_path.exists():
            raise FileNotFoundError(
                f"Required file not found: {file_path}"
            )


# --------------------------------------------------
# Create video
# --------------------------------------------------

def create_video(config):

    video_config = config["video"]
    audio_config = config["audio"]
    input_config = config["inputs"]
    output_config = config["output"]

    # ----------------------------------------------
    # Resolve input files
    # ----------------------------------------------

    audio_file = resolve_project_path(
        input_config["audio"]
    )

    srt_file = resolve_project_path(
        input_config["subtitles"]
    )

    background_file = resolve_project_path(
        input_config["background"]
    )

    # ----------------------------------------------
    # Resolve output
    # ----------------------------------------------

    output_dir = resolve_project_path(
        output_config["directory"]
    )

    output_file = (
        output_dir /
        output_config["filename"]
    )

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # ----------------------------------------------
    # Check files
    # ----------------------------------------------

    check_files(
        audio_file,
        srt_file,
        background_file
    )

    # ----------------------------------------------
    # Read video settings
    # ----------------------------------------------

    width = video_config["width"]
    height = video_config["height"]
    fps = video_config["fps"]

    video_codec = video_config["video_codec"]
    pixel_format = video_config["pixel_format"]
    video_quality = video_config["video_quality"]
    preset = video_config["preset"]

    # ----------------------------------------------
    # Read audio settings
    # ----------------------------------------------

    audio_codec = audio_config["audio_codec"]
    audio_bitrate = audio_config["bitrate"]

    # ----------------------------------------------
    # Subtitle path
    # ----------------------------------------------

    subtitle_path = prepare_subtitle_path(
        srt_file
    )

    # ----------------------------------------------
    # Display configuration
    # ----------------------------------------------

    print("=" * 60)
    print("LOCAL AI VIDEO AUTOMATION")
    print("Day 6 - Configuration Driven Video Assembly")
    print("=" * 60)

    print()
    print("VIDEO SETTINGS")
    print("-" * 60)
    print(f"Resolution   : {width}x{height}")
    print(f"FPS          : {fps}")
    print(f"Video codec  : {video_codec}")
    print(f"Pixel format : {pixel_format}")
    print(f"Quality      : {video_quality}")
    print(f"Preset       : {preset}")

    print()
    print("AUDIO SETTINGS")
    print("-" * 60)
    print(f"Audio codec  : {audio_codec}")
    print(f"Bitrate      : {audio_bitrate}")

    print()
    print("INPUT FILES")
    print("-" * 60)
    print(f"Audio        : {audio_file}")
    print(f"Subtitles    : {srt_file}")
    print(f"Background   : {background_file}")

    print()
    print("OUTPUT")
    print("-" * 60)
    print(f"Video        : {output_file}")
    print()

    # ----------------------------------------------
    # FFmpeg command
    # ----------------------------------------------

    command = [
        "ffmpeg",
        "-y",

        # Background image
        "-loop",
        "1",

        "-framerate",
        str(fps),

        "-i",
        str(background_file.resolve()),

        # Narration
        "-i",
        str(audio_file.resolve()),

        # Subtitles
        "-vf",
        f"subtitles='{subtitle_path}'",

        # Video encoding
        "-c:v",
        video_codec,

        "-preset",
        preset,

        "-crf",
        str(video_quality),

        "-pix_fmt",
        pixel_format,

        # Audio encoding
        "-c:a",
        audio_codec,

        "-b:a",
        audio_bitrate,

        # Stop when audio ends
        "-shortest",

        str(output_file.resolve()),
    ]

    print("Running FFmpeg...")
    print()

    subprocess.run(
        command,
        check=True
    )

    print()
    print("=" * 60)
    print("VIDEO CREATED SUCCESSFULLY")
    print("=" * 60)
    print(f"Output: {output_file}")


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    config = load_config()

    create_video(config)


if __name__ == "__main__":
    main()