from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = (
    PROJECT_ROOT
    / "assets"
    / "visuals"
    / "generated"
)

OUTPUT_FILE = OUTPUT_DIR / "scene_05_transition.png"


WIDTH = 1920
HEIGHT = 1080

TITLE = "Let's Continue"
CHANNEL = "YOGESHTECHCODE"


def load_font(size):
    font_paths = [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibri.ttf"
    ]

    for path in font_paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)

    return ImageFont.load_default()


def create_transition_visual():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        (18, 18, 24)
    )

    draw = ImageDraw.Draw(image)

    title_font = load_font(86)
    channel_font = load_font(32)

    title_box = draw.textbbox(
        (0, 0),
        TITLE,
        font=title_font
    )

    title_width = title_box[2] - title_box[0]
    title_height = title_box[3] - title_box[1]

    title_x = (WIDTH - title_width) // 2
    title_y = (HEIGHT - title_height) // 2

    draw.text(
        (title_x, title_y),
        TITLE,
        font=title_font,
        fill=(255, 255, 255)
    )

    channel_box = draw.textbbox(
        (0, 0),
        CHANNEL,
        font=channel_font
    )

    channel_width = channel_box[2] - channel_box[0]

    channel_x = (WIDTH - channel_width) // 2

    draw.text(
        (channel_x, HEIGHT - 75),
        CHANNEL,
        font=channel_font,
        fill=(160, 160, 160)
    )

    image.save(
        OUTPUT_FILE,
        format="PNG"
    )

    print("Transition visual created successfully:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    create_transition_visual()