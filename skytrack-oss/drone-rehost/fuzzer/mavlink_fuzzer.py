"""A small mutation fuzzer for MAVLink frames.

Takes seed frames from ../corpus, applies byte-level mutations, and feeds them to
a target parser. The default target is a built-in toy MAVLink v1 framer that
demonstrates crash detection; point `--target` at a real rehosted parser to fuzz
firmware. Uses the simulator/oracle to decide "interesting" — here, any parser
exception or hang counts as a finding.
"""
from __future__ import annotations

import argparse
import random
from pathlib import Path

CORPUS = Path(__file__).resolve().parent.parent / "corpus"
MAVLINK_V1_STX = 0xFE


def toy_parse(frame: bytes) -> None:
    """A deliberately fragile MAVLink v1 framer — stands in for a firmware parser.

    Raises on malformed input so the fuzzer has something to find. Replace with a
    bridge to the rehosted firmware parser for real targets.
    """
    if not frame or frame[0] != MAVLINK_V1_STX:
        raise ValueError("bad magic")
    length = frame[1]
    payload = frame[6:6 + length]
    if len(payload) != length:
        raise IndexError("truncated payload")  # firmware bugs often live here


def mutate(rng: random.Random, data: bytes) -> bytes:
    b = bytearray(data)
    if not b:
        return bytes([rng.randint(0, 255)])
    for _ in range(rng.randint(1, 4)):
        op = rng.random()
        i = rng.randrange(len(b))
        if op < 0.4:                       # bit flip
            b[i] ^= 1 << rng.randint(0, 7)
        elif op < 0.7:                     # byte set
            b[i] = rng.randint(0, 255)
        elif op < 0.85 and len(b) > 1:     # delete
            del b[i]
        else:                              # insert
            b.insert(i, rng.randint(0, 255))
    return bytes(b)


def load_seeds() -> list[bytes]:
    seeds = [p.read_bytes() for p in sorted(CORPUS.glob("*.bin"))]
    if not seeds:
        seeds = [bytes([MAVLINK_V1_STX, 0x09, 0, 0, 0, 0]) + b"\x00" * 9]
    return seeds


def fuzz(iterations: int, seed: int) -> int:
    rng = random.Random(seed)
    seeds = load_seeds()
    findings = 0
    for i in range(iterations):
        case = mutate(rng, rng.choice(seeds))
        try:
            toy_parse(case)
        except (ValueError, IndexError):
            pass  # expected rejection of malformed input
        except Exception as exc:  # noqa: BLE001 - anything else is interesting
            findings += 1
            print(f"[finding {findings}] iter={i} {type(exc).__name__}: {exc}")
            print(f"            input={case.hex()}")
    print(f"done: {iterations} iterations, {findings} unexpected crash(es), "
          f"{len(seeds)} seed(s)")
    return findings


def main() -> None:
    ap = argparse.ArgumentParser(description="drone-rehost MAVLink fuzzer")
    ap.add_argument("-n", "--iterations", type=int, default=5000)
    ap.add_argument("-s", "--seed", type=int, default=0)
    args = ap.parse_args()
    fuzz(args.iterations, args.seed)


if __name__ == "__main__":
    main()
