from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = (
    PROJECT_ROOT
    / "assets"
    / "visuals"
    / "generated"
)

OUTPUT_FILE = OUTPUT_DIR / "scene_04_code.png"


WIDTH = 1920
HEIGHT = 1080

CHANNEL = "YOGESHTECHCODE"

CODE = """SELECT
    customer_id,
    SUM(amount) AS total_amount
FROM loan_transactions
GROUP BY customer_id
ORDER BY total_amount DESC;
"""


def load_font(size):
    font_paths = [
        "C:/Windows/Fonts/consola.ttf",
        "C:/Windows/Fonts/cour.ttf",
        "C:/Windows/Fonts/arial.ttf"
    ]

    for path in font_paths:
        if Path(path).exists():
            return ImageFont.truetype(path, size)

    return ImageFont.load_default()


def create_code_visual():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        (18, 18, 24)
    )

    draw = ImageDraw.Draw(image)

    title_font = load_font(52)
    code_font = load_font(34)
    channel_font = load_font(30)

    title = "SQL Analytics Example"

    title_box = draw.textbbox(
        (0, 0),
        title,
        font=title_font
    )

    title_width = title_box[2] - title_box[0]

    draw.text(
        ((WIDTH - title_width) // 2, 70),
        title,
        font=title_font,
        fill=(255, 255, 255)
    )

    code_x = 180
    code_y = 220

    line_height = 55

    for index, line in enumerate(CODE.splitlines()):
        draw.text(
            (code_x, code_y + index * line_height),
            line,
            font=code_font,
            fill=(230, 230, 230)
        )

    channel_box = draw.textbbox(
        (0, 0),
        CHANNEL,
        font=channel_font
    )

    channel_width = channel_box[2] - channel_box[0]

    draw.text(
        ((WIDTH - channel_width) // 2, HEIGHT - 70),
        CHANNEL,
        font=channel_font,
        fill=(160, 160, 160)
    )

    image.save(
        OUTPUT_FILE,
        format="PNG"
    )

    print("Code visual created successfully:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    create_code_visual()