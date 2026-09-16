import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from simulator.pet_sim import run_demo


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline AI pet Mac brain")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("demo", help="run the hardware-independent behavior demo")
    args = parser.parse_args()
    if args.command == "demo":
        run_demo()


if __name__ == "__main__":
    main()
