# Secret-Escrow 🤫

A prototype implementation of escrow information concealment using joux's Tripartite-Diffie-Hellman.

## Dependencies

- [Python3](https://www.python.org/downloads/)
  - v3.11
- [ethereum/py_ecc](https://github.com/ethereum/py_ecc)
  - bls12_381 curve operations
- [Solidity](https://docs.soliditylang.org/)
  - We are using Solidity to implement our smart contracts. 
  - Currently, we are using v0.8.23.
- [eth-brownie](https://github.com/eth-brownie/brownie)
  - We are using the eth-brownie framework for developing and testing our contracts.
- [OpenZeppelin](https://openzeppelin.com/contracts/)
  - Our project is partly dependent on OpenZeppelin.
  - We use openzeppelin-contracts v4.9.

## Install

Install 3rd party packages.

```bash
$ make install
```

Install openzeppelin-contracts.

```bash
$ brownie pm install OpenZeppelin/openzeppelin-contracts@4.9.3
```

## Compile Contracts

```bash
$ make compile
```
If the compilation is successful, an ABI will be generated under the `build/` directory.

## Run test

After compiling, Run the following command:
```bash
$ make test
```

## References
1. Joux, A. (2000). A One Round Protocol for Tripartite Diffie–Hellman. In: Bosma, W. (eds) Algorithmic Number Theory. ANTS 2000. Lecture Notes in Computer Science, vol 1838. Springer, Berlin, Heidelberg. https://doi.org/10.1007/10722028_23
