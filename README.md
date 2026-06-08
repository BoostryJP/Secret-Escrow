# Secret-Escrow 🤫

A prototype implementation of escrow information concealment using Joux's Tripartite-Diffie-Hellman.

## Dependencies

- [Python](https://www.python.org/downloads/)
  - v3.14
- [Ape Framework](https://www.apeworx.io/ape/stable/)
  - We use Ape with the Solidity and Foundry plugins for contract compilation and testing.
- [ethereum/py_ecc](https://github.com/ethereum/py_ecc)
  - bls12_381 curve operations
- [Solidity](https://docs.soliditylang.org/)
  - We are using Solidity to implement our smart contracts.
  - Currently, we are using v0.8.34.
- [Anvil](https://www.getfoundry.sh/anvil)
  - We use Anvil for local development and unit testing.
- [OpenZeppelin](https://openzeppelin.com/contracts/)
  - Our project is partly dependent on OpenZeppelin.
  - We use openzeppelin-contracts v4.9.

## Install

### Create virtual environment
```bash
$ uv venv
```

### Install packages

Install 3rd party packages.
```bash
$ make install
```

Install Ape dependencies.
```bash
$ make setup
```

## Compile Contracts

```bash
$ make compile
```
If compilation succeeds, Ape writes the build manifest under `.build/`.

## Run test

After compiling, run the following command:
```bash
$ make test
```

To run a specific test file:
```bash
$ make test {path_to_test_file}
```

## Developing Smart Contracts

### Network(Anvil) settings

The Ape project settings are defined in `ape-config.yaml`.

The Anvil command used for tests is defined in `tests/run_anvil_test.sh` and uses chain ID `2017` to match the app-side transaction builder.

## References
1. Joux, A. (2000). A One Round Protocol for Tripartite Diffie–Hellman. In: Bosma, W. (eds) Algorithmic Number Theory. ANTS 2000. Lecture Notes in Computer Science, vol 1838. Springer, Berlin, Heidelberg. https://doi.org/10.1007/10722028_23
