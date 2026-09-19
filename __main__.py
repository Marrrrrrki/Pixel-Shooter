import subprocess
import sys
import os


folder = os.path.dirname(
    os.path.abspath(__file__)
)


print("Creating upgrade icons...")

result = subprocess.run(
    [
        sys.executable,
        os.path.join(
            folder,
            "make_upgrade_icons.py"
        )
    ]
)

if result.returncode != 0:

    print()
    print("make_upgrade_icons.py failed.")
    input("Press Enter to exit...")
    sys.exit(result.returncode)


print()
print("Starting Pixel Shooter...")
print()

subprocess.run(
    [
        sys.executable,
        os.path.join(
            folder,
            "main.py"
        )
    ]
)