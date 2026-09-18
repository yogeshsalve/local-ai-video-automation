import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SCENE_FILE = (
    PROJECT_ROOT
    / "assets"
    / "scenes"
    / "generated"
    / "microsoft_fabric_lakehouse_scenes.json"
)

CONFIG_FILE = (
    PROJECT_ROOT
    / "config"
    / "visual_config.json"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "assets"
    / "visuals"
    / "generated"
)


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def create_visual_manifest(scene_plan, visual_config):
    manifest = []

    channel_name = visual_config["branding"]["channel_name"]

    for scene in scene_plan["scenes"]:
        scene_number = scene["scene_number"]
        visual_type = scene["visual_type"]
        description = scene["visual_description"]

        manifest.append(
            {
                "scene_number": scene_number,
                "visual_type": visual_type,
                "visual_description": description,
                "channel_name": channel_name,
                "output_file": (
                    f"scene_{scene_number:02d}_{visual_type}.png"
                ),
            }
        )

    return manifest


def save_manifest(manifest):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_DIR / "visual_manifest.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(
            manifest,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print()
    print("Visual manifest saved successfully:")
    print(output_file)

    return output_file


def main():
    print("Creating visual manifest...")
    print()

    scene_plan = load_json(SCENE_FILE)
    visual_config = load_json(CONFIG_FILE)

    manifest = create_visual_manifest(
        scene_plan,
        visual_config,
    )

    print("=" * 60)
    print("VISUAL MANIFEST")
    print("=" * 60)
    print()

    print(json.dumps(manifest, indent=2, ensure_ascii=False))

    save_manifest(manifest)


if __name__ == "__main__":
    main()