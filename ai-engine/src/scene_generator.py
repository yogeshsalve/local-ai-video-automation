import json
import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

PROMPT_FILE = PROJECT_ROOT / "config" / "scene_prompt.txt"
SCRIPT_FILE = (
    PROJECT_ROOT
    / "assets"
    / "scripts"
    / "generated"
    / "microsoft_fabric_lakehouse_script.txt"
)

OUTPUT_DIR = PROJECT_ROOT / "assets" / "scenes" / "generated"

MODEL_NAME = "qwen2.5:3b"


def load_prompt(script):
    if not PROMPT_FILE.exists():
        raise FileNotFoundError(f"Prompt file not found: {PROMPT_FILE}")

    prompt_template = PROMPT_FILE.read_text(encoding="utf-8")

    return prompt_template.replace("{script}", script)


def generate_scene_plan(script):
    prompt = load_prompt(script)

    command = [
        "ollama",
        "run",
        MODEL_NAME,
        prompt,
    ]

    print("Generating scene plan with local AI...")
    print(f"Model : {MODEL_NAME}")
    print()

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )

    return result.stdout.strip()


def parse_scene_text(text):
    scenes = []
    current_scene = {}

    for raw_line in text.splitlines():
        line = raw_line.strip()
        line = line.replace("\x1b", "")

        if not line:
            continue

        if line.startswith("SCENE_NUMBER:"):
            if current_scene:
                scenes.append(current_scene)

            current_scene = {
                "scene_number": int(
                    line.split(":", 1)[1].strip()
                )
            }

        elif line.startswith("NARRATION:"):
            current_scene["narration"] = (
                line.split(":", 1)[1].strip()
            )

        elif line.startswith("VISUAL_TYPE:"):
            current_scene["visual_type"] = (
                line.split(":", 1)[1].strip()
            )

        elif line.startswith("VISUAL_DESCRIPTION:"):
            current_scene["visual_description"] = (
                line.split(":", 1)[1].strip()
            )

        elif line.startswith("DURATION:"):
            current_scene["estimated_duration_seconds"] = int(
                line.split(":", 1)[1].strip()
            )

    if current_scene:
        scenes.append(current_scene)

    if not scenes:
        raise ValueError("No scenes found in AI response.")

    for scene in scenes:
        required_fields = [
            "scene_number",
            "narration",
            "visual_type",
            "visual_description",
            "estimated_duration_seconds",
        ]

        for field in required_fields:
            if field not in scene:
                raise ValueError(
                    f"Scene {scene.get('scene_number', '?')} "
                    f"is missing field: {field}"
                )

    return {
        "title": "Microsoft Fabric Lakehouse",
        "scenes": scenes,
    }

def save_scene_plan(scene_plan):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_DIR / "microsoft_fabric_lakehouse_scenes.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(
            scene_plan,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print("Scene plan saved successfully:")
    print(output_file)

    return output_file


def main():
    if not SCRIPT_FILE.exists():
        raise FileNotFoundError(
            f"Script file not found: {SCRIPT_FILE}"
        )

    script = SCRIPT_FILE.read_text(encoding="utf-8")

    raw_scene_plan = generate_scene_plan(script)

    debug_file = OUTPUT_DIR / "debug_raw_scene_response.txt"
    debug_file.write_text(raw_scene_plan, encoding="utf-8")

    print()
    print(f"Raw AI response saved to:")
    print(debug_file)
    print()

    scene_plan = parse_scene_text(raw_scene_plan)

    print("=" * 60)
    print("VALIDATED SCENE PLAN")
    print("=" * 60)
    print()
    print(json.dumps(scene_plan, indent=2, ensure_ascii=False))
    print()

    save_scene_plan(scene_plan)


if __name__ == "__main__":
    main()