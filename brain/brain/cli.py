import argparse
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from simulator.pet_sim import run_demo
from brain.server import run_server


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline AI pet Mac brain")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("demo", help="run the hardware-independent behavior demo")
    sub.add_parser("server", help="run the local Mac WebSocket brain")
    args = parser.parse_args()
    if args.command == "demo":
        run_demo()
    elif args.command == "server":
        asyncio.run(run_server())


if __name__ == "__main__":
    main()
