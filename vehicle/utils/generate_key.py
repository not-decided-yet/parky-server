"""Generates the key."""
import argparse
import os

from Crypto.PublicKey import RSA

# fmt: off
parser = argparse.ArgumentParser()
parser.add_argument("path", type=str, help="Path to export keys")
parser.add_argument("-b", "--bits", type=int, default=2048, help="Bits for RSA")
# fmt: on


def main(args: argparse.Namespace):
    print("Arguments:")
    print(f"\tPath: {args.path}")
    print(f"\tBits: {args.bits}")

    key = RSA.generate(args.bits)
    private_key = key.export_key("PEM")
    public_key = key.publickey().exportKey("PEM")

    with open(os.path.join(args.path, "key"), "w", encoding="utf-8") as f:
        f.write(private_key.decode("utf-8"))

    with open(os.path.join(args.path, "key.pub"), "w", encoding="utf-8") as f:
        f.write(public_key.decode("utf-8"))


if __name__ == "__main__":
    exit(main(parser.parse_args()))
