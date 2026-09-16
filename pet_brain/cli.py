import argparse
import asyncio

from pet_brain.server import run_server
from simulator.pet_sim import run_demo

def main() -> None:
    parser = argparse.ArgumentParser(description="Offline AI pet Mac brain")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("demo")
    sub.add_parser("server")
    args = parser.parse_args()
    if args.command == "demo": run_demo()
    else: asyncio.run(run_server())

if __name__ == "__main__": main()
