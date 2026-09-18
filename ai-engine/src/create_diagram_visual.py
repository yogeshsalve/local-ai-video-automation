from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_DIR = (
    PROJECT_ROOT
    / "assets"
    / "visuals"
    / "generated"
)

OUTPUT_FILE = OUTPUT_DIR / "scene_03_diagram.png"


WIDTH = 1920
HEIGHT = 1080

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


def centered_text(draw, text, y, font, fill):
    box = draw.textbbox((0, 0), text, font=font)

    text_width = box[2] - box[0]

    x = (WIDTH - text_width) // 2

    draw.text(
        (x, y),
        text,
        font=font,
        fill=fill
    )


def create_diagram_visual():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    image = Image.new(
        "RGB",
        (WIDTH, HEIGHT),
        (18, 18, 24)
    )

    draw = ImageDraw.Draw(image)

    title_font = load_font(62)
    box_font = load_font(34)
    channel_font = load_font(30)

    centered_text(
        draw,
        "Microsoft Fabric Lakehouse",
        80,
        title_font,
        (255, 255, 255)
    )

    boxes = [
        "Data Sources",
        "Data Lake",
        "Lakehouse",
        "SQL Analytics",
        "Advanced Analytics"
    ]

    box_width = 500
    box_height = 95

    start_y = 220
    gap = 45

    for index, label in enumerate(boxes):

        y = start_y + index * (box_height + gap)

        x = (WIDTH - box_width) // 2

        draw.rounded_rectangle(
            (x, y, x + box_width, y + box_height),
            radius=20,
            outline=(220, 220, 220),
            width=3
        )

        text_box = draw.textbbox(
            (0, 0),
            label,
            font=box_font
        )

        text_width = text_box[2] - text_box[0]
        text_height = text_box[3] - text_box[1]

        text_x = x + (box_width - text_width) // 2
        text_y = y + (box_height - text_height) // 2

        draw.text(
            (text_x, text_y),
            label,
            font=box_font,
            fill=(255, 255, 255)
        )

        if index < len(boxes) - 1:

            arrow_x = WIDTH // 2

            arrow_start_y = y + box_height
            arrow_end_y = y + box_height + gap

            draw.line(
                (
                    arrow_x,
                    arrow_start_y,
                    arrow_x,
                    arrow_end_y
                ),
                fill=(180, 180, 180),
                width=4
            )

            draw.polygon(
                [
                    (
                        arrow_x - 10,
                        arrow_end_y - 12
                    ),
                    (
                        arrow_x + 10,
                        arrow_end_y - 12
                    ),
                    (
                        arrow_x,
                        arrow_end_y
                    )
                ],
                fill=(180, 180, 180)
            )

    centered_text(
        draw,
        CHANNEL,
        HEIGHT - 70,
        channel_font,
        (160, 160, 160)
    )

    image.save(
        OUTPUT_FILE,
        format="PNG"
    )

    print("Diagram visual created successfully:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    create_diagram_visual()