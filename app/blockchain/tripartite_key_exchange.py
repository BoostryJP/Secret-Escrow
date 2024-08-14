import secrets
from hashlib import sha256

from py_ecc.bls12_381 import G1, G2, curve_order, multiply, pairing
from py_ecc.fields import bls12_381_FQ, bls12_381_FQ2, bls12_381_FQ12
from pydantic import BaseModel

from app.blockchain.type.eth_account import EOA
from app.utils.contract_utils import ContractUtils
from config import CHAIN_ID, TX_GAS_LIMIT


class TKERegisterPublicKeyParams(BaseModel):
    g1pk_11: str
    g1pk_12: str
    g2pk_11: str
    g2pk_12: str
    g2pk_21: str
    g2pk_22: str


class TripartiteKeyExchangeContract:

    def __init__(self, account: EOA, contract_address: str):
        self.key_exchange_contract = ContractUtils.get_contract(
            contract_name="TripartiteKeyExchange", contract_address=contract_address
        )
        self.account = account

    @staticmethod
    def generate_key():
        sk = int.from_bytes(secrets.token_bytes(32)) % curve_order
        g1pk: tuple[bls12_381_FQ, bls12_381_FQ] = multiply(G1, sk)
        g2pk: tuple[bls12_381_FQ2, bls12_381_FQ2] = multiply(G2, sk)
        return sk, g1pk, g2pk

    def register_public_key(self, public_key: TKERegisterPublicKeyParams):
        tx = self.key_exchange_contract.functions.registerPublicKey(
            public_key.g1pk_11,
            public_key.g1pk_12,
            public_key.g2pk_11,
            public_key.g2pk_12,
            public_key.g2pk_21,
            public_key.g2pk_22,
        ).build_transaction(
            {
                "chainId": CHAIN_ID,
                "from": self.account.address,
                "gas": TX_GAS_LIMIT,
                "gasPrice": 0,
            }
        )
        tx_hash, tx_receipt = ContractUtils.send_transaction(
            transaction=tx, private_key=self.account.private_key
        )
        return tx_hash, tx_receipt

    def get_G1_public_key(self, address: str):
        g1pk = self.key_exchange_contract.functions.G1PK(address).call()
        return g1pk

    def get_G2_public_key(self, address: str):
        g2pk = self.key_exchange_contract.functions.G2PK(address).call()
        return g2pk

    def generate_shared_key(self, secret_key, address1: str, address2: str):
        Q: tuple[bls12_381_FQ2, bls12_381_FQ2]
        P: tuple[bls12_381_FQ, bls12_381_FQ]

        address1_g2pk = self.get_G2_public_key(address1)
        Q = (
            bls12_381_FQ2([int(address1_g2pk[0]), int(address1_g2pk[1])]),
            bls12_381_FQ2([int(address1_g2pk[2]), int(address1_g2pk[3])]),
        )

        address2_g1pk = self.get_G1_public_key(address2)
        P = (
            bls12_381_FQ(int(address2_g1pk[0])),
            bls12_381_FQ(int(address2_g1pk[1])),
        )

        dh_paring: bls12_381_FQ12 = pairing(Q, P) ** secret_key
        _hash = sha256()
        for _item in dh_paring.coeffs:
            _item = int(_item)
            _hash.update(_item.to_bytes(48))
        shared_key = _hash.digest()
        return shared_key
