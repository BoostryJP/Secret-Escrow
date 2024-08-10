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
Use eth-brownie to compile contracts.

```bash
$ brownie compile
```

## Sample results :test_tube:

#### sandbox/tripartite_dh_sample.py

```

== Generate Alice's key ==

<A_sk>
48504464656614128748810727505606585212970767068906776632677249187557527048250
<A_pk1>
(3601029079103801678979025001108635334613321544325901274257453117702517675214350313718994239699519999636729757754629, 2238296275487970299483943455774669729169336608074610195174438775154719770606697208882042383629001884826124197256886)
<A_pk2>
((2561012464168234979130851503615979002752529580374144003338916913719963523386666641995900377434825947332841177782710, 1625247846228801585179289607617905082129925459494353477574525843496329720078402835823620191947142044233110618779704), (3824377781434581801001727407835743236566695867997478732780641281041468859132433236708030948491108581581302721130715, 1377706417334059720462638002155418041825964943144504148692399945980221580712450904385058476128683311324197269697583))

== Generate Bob's key ==

<B_sk>
40288250903959579448820836679410228355913648670489351256818820822521235248701
<B_pk1>
(3356735120633373049663130374308083808795522095609875855458190998405887266445935890814000970152868143984887384773943, 2280926727930834384135180452010215605131849073082575977873235209386181093588302511385185150196013877444124789175028)
<B_pk2>
((2620974888820748407525796563321484074787726548682618721598736274600855821466694404015979038485055834645446753146139, 73260787367930164835799623752580265363888627970287212690965704834784227655341680789270936627147887281885520258862), (628467644707876290313022267356408262665131956447827514403635859241849697513942793356943620307925421048660665960875, 1361004819137264641596626279204853734990256100116281076819877496782807600739879656862408842741467268266555751944067))

== Generate Charlie's key ==

<C_sk>
63353670399073836276860774037432655242828171491371706780246216361850426009438
<C_pk1>
(1906946131163144000327100792177302129053893946831549096477067786342831993994363293977270178443666560604027919333345, 2283954454961374306711641446138621066898140232633346083563046776615887758553058257855539158363603253984998866501437)
<C_pk2>
((1791673516695938761332252421477683194810662207720825861155146329725763113377706813766203325358206756103940398339955, 792996710367094440910564928238136424041389738973208747709827726572450346247348714614295752620949645936129751156833), (1761082772504728541152061195770293848358751187458530876824700302945800124802145355852259783609891079832256073155724, 541197048271156535412330463556188378792827842222211353145174874053648556067361287456161444612659756966672271301694))

== DH key (Alice) ==

b'\xcd\x08\xc8\xd6>V\xf0\x8e\xfb\xdc\\\x0c\xdbt\xb9\xac\xf3\xeb\x13Ba<\x85\xbeC\xcd\xe8\x1c9Yyk'

== DH key (Bob) ==

b'\xcd\x08\xc8\xd6>V\xf0\x8e\xfb\xdc\\\x0c\xdbt\xb9\xac\xf3\xeb\x13Ba<\x85\xbeC\xcd\xe8\x1c9Yyk'

== DH key (Charlie) ==

b'\xcd\x08\xc8\xd6>V\xf0\x8e\xfb\xdc\\\x0c\xdbt\xb9\xac\xf3\xeb\x13Ba<\x85\xbeC\xcd\xe8\x1c9Yyk'

!!! Result !!!

A_shared_key == B_shared_key == C_shared_key -> True
Original message = 'A One Round Protocol for Tripartite Diffie–Hellman'
Encrypted message = cAY1b8wO/UMiDtS/QttNKi6e2E4WFNWYGcdvZ4CRxVAN2FOgdrMW1Y1DZYeMhBwJNSn5MBa+XswCulvpTOoMikVD94xzsTbiaenHRYXZ7OQ=
```

## References
1. Antoine Joux, A one round protocol for tripartite Diffie-Hellman. Journal of Cryptology
