from pathlib import Path
import subprocess
import sys
import json


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MANIFEST_FILE = (
    PROJECT_ROOT
    / "assets"
    / "visuals"
    / "generated"
    / "visual_manifest.json"
)

GENERATORS = {
    "title": "create_title_visual.py",
    "text": "create_text_visual.py",
    "diagram": "create_diagram_visual.py",
    "code": "create_code_visual.py",
    "transition": "create_transition_visual.py",
}


def load_manifest():
    with open(MANIFEST_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def run_generator(visual_type):
    if visual_type not in GENERATORS:
        print(
            f"Skipping unsupported visual type: {visual_type}"
        )
        return

    generator_file = GENERATORS[visual_type]

    generator_path = (
        PROJECT_ROOT
        / "ai-engine"
        / "src"
        / generator_file
    )

    print()
    print(f"Visual type : {visual_type}")
    print(f"Generator   : {generator_file}")

    result = subprocess.run(
        [sys.executable, str(generator_path)],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr)

        raise RuntimeError(
            f"Generator failed: {generator_file}"
        )

    print(result.stdout.strip())


def main():
    print("=" * 60)
    print("MASTER VISUAL GENERATOR")
    print("=" * 60)

    manifest = load_manifest()

    scenes = manifest

    for scene in scenes:
        visual_type = scene["visual_type"]

        run_generator(visual_type)

    print()
    print("=" * 60)
    print("ALL MANIFEST VISUALS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()