import subprocess
from pathlib import Path


OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

output_file = OUTPUT_DIR / "day2_test.mp4"

command = [
    "ffmpeg",
    "-y",
    "-f", "lavfi",
    "-i", "color=c=black:s=1920x1080:d=5",
    "-vf",
    "drawtext=text='YOGESHTECHCODE':"
    "fontcolor=white:"
    "fontsize=80:"
    "x=(w-text_w)/2:"
    "y=(h-text_h)/2",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    str(output_file),
]

print("Creating test video...")

subprocess.run(command, check=True)

print(f"Video created successfully: {output_file}")