import sys
import subprocess
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PROMPT_FILE = PROJECT_ROOT / "config" / "script_prompt.txt"
OUTPUT_DIR = PROJECT_ROOT / "assets" / "scripts" / "generated"

MODEL_NAME = "qwen2.5:3b"


def load_prompt(topic):
    if not PROMPT_FILE.exists():
        raise FileNotFoundError(f"Prompt file not found: {PROMPT_FILE}")

    prompt_template = PROMPT_FILE.read_text(encoding="utf-8")

    return prompt_template.replace("{topic}", topic)


def generate_script(topic):
    prompt = load_prompt(topic)

    command = [
        "ollama",
        "run",
        MODEL_NAME,
        prompt,
    ]

    print("Generating script with local AI...")
    print(f"Model : {MODEL_NAME}")
    print(f"Topic : {topic}")
    print()

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )

    return result.stdout.strip()


def save_script(script, topic):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    safe_topic = "".join(
        character.lower() if character.isalnum() else "_"
        for character in topic
    )

    while "__" in safe_topic:
        safe_topic = safe_topic.replace("__", "_")

    safe_topic = safe_topic.strip("_")

    output_file = OUTPUT_DIR / f"{safe_topic}_script.txt"

    output_file.write_text(
        script,
        encoding="utf-8",
    )

    print()
    print("Script saved successfully:")
    print(output_file)

    return output_file

def main():
    if len(sys.argv) < 2:
        print("Usage: python ai-engine\\src\\script_generator.py \"Your topic\"")
        return

    topic = " ".join(sys.argv[1:])

    script = generate_script(topic)

    print("=" * 60)
    print("GENERATED YOUTUBE SCRIPT")
    print("=" * 60)
    print()
    print(script)

    save_script(script, topic)


if __name__ == "__main__":
    main()