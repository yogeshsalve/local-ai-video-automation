from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = (
    PROJECT_ROOT
    / "assets"
    / "visuals"
    / "generated"
)

OUTPUT_FILE = OUTPUT_DIR / "scene_02_text.png"


WIDTH = 1920
HEIGHT = 1080

TITLE = "Data Across Different Systems"
DESCRIPTION = "Customer data • Sales data • Application data"
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


def create_text_visual():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        (18, 18, 24)
    )

    draw = ImageDraw.Draw(image)

    title_font = load_font(72)
    description_font = load_font(42)
    channel_font = load_font(32)

    title_box = draw.textbbox(
        (0, 0),
        TITLE,
        font=title_font
    )

    title_width = title_box[2] - title_box[0]
    title_height = title_box[3] - title_box[1]

    title_x = (WIDTH - title_width) // 2
    title_y = 360

    draw.text(
        (title_x, title_y),
        TITLE,
        font=title_font,
        fill=(255, 255, 255)
    )

    description_box = draw.textbbox(
        (0, 0),
        DESCRIPTION,
        font=description_font
    )

    description_width = (
        description_box[2] - description_box[0]
    )

    description_x = (
        WIDTH - description_width
    ) // 2

    description_y = title_y + title_height + 50

    draw.text(
        (description_x, description_y),
        DESCRIPTION,
        font=description_font,
        fill=(190, 190, 190)
    )

    channel_box = draw.textbbox(
        (0, 0),
        CHANNEL,
        font=channel_font
    )

    channel_width = channel_box[2] - channel_box[0]

    channel_x = (WIDTH - channel_width) // 2
    channel_y = HEIGHT - 100

    draw.text(
        (channel_x, channel_y),
        CHANNEL,
        font=channel_font,
        fill=(160, 160, 160)
    )

    image.save(
        OUTPUT_FILE,
        format="PNG"
    )

    print("Text visual created successfully:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    create_text_visual()