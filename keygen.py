import argparse
import typing
from dataclasses import dataclass

from iroha import IrohaCrypto


@dataclass
class Key:
    value: bytes
    name: str


def generate_keypair(name: str) -> typing.Iterable[Key]:
    private_key = Key(
        name=f"{name}.priv",
        value=IrohaCrypto.private_key(),
    )
    yield private_key
    yield Key(
        name=f"{name}.pub",
        value=IrohaCrypto.derive_public_key(private_key.value),
    )


def main(*, name: str, **kwargs: typing.Dict[str, str]) -> None:
    for key in generate_keypair(name):
        with open(key.name, "wb") as f:
            f.write(key.value)
        print(f"🔒 Wrote key {key.name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        argument_default=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--name",
        help="keypair name",
        required=True,
    )
    main(**vars(parser.parse_args()))
