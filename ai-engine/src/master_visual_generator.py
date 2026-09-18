from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]

GENERATORS = {
    "title": "create_title_visual.py",
    "text": "create_text_visual.py",
    "diagram": "create_diagram_visual.py",
    "code": "create_code_visual.py",
    "transition": "create_transition_visual.py",
}


def run_generator(generator_file):
    generator_path = PROJECT_ROOT / "ai-engine" / "src" / generator_file

    print()
    print(f"Running: {generator_file}")

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

    for visual_type, generator_file in GENERATORS.items():
        print()
        print(f"Visual type: {visual_type}")

        run_generator(generator_file)

    print()
    print("=" * 60)
    print("ALL VISUAL GENERATORS COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    main()