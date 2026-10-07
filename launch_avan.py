import os
import sys
import subprocess

ROOT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

PYTHON = sys.executable


def main():
    # Start Avan HUD
    hud = subprocess.Popen(
        [
            PYTHON,
            os.path.join(
                ROOT_DIR,
                "ui",
                "avan_hud.py"
            )
        ],
        cwd=ROOT_DIR
    )

    # Start Avan AI
    avan = subprocess.Popen(
        [
            PYTHON,
            os.path.join(
                ROOT_DIR,
                "main.py"
            )
        ],
        cwd=ROOT_DIR
    )

    try:
        hud.wait()
        avan.wait()

    except KeyboardInterrupt:
        print("\n🛑 Closing Avan AI...")

    finally:
        for process in (hud, avan):
            if process.poll() is None:
                process.terminate()

        print("✅ Avan AI closed.")


if __name__ == "__main__":
    main()