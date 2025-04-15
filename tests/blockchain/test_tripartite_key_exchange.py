import secrets

import pytest
from coincurve import PublicKey
from eth_utils import keccak, to_checksum_address

from app.blockchain.tripartite_key_exchange import (
    TKERegisterPublicKeyParams,
    TripartiteKeyExchangeContract,
)
from app.blockchain.type.eth_account import EOA
from app.exceptions import KeyNotRegisteredError


def get_eth_key():
    private_key = keccak(secrets.token_bytes(32))
    public_key = PublicKey.from_valid_secret(private_key).format(compressed=False)[1:]
    eth_addr = to_checksum_address(keccak(public_key)[-20:])
    return EOA(address=eth_addr, private_key=private_key)


class TestRegisterPublicKey:
    def test_register(self, key_exchange):
        user = get_eth_key()

        ke_model = TripartiteKeyExchangeContract(
            account=user, contract_address=key_exchange.address
        )
        sk, g1pk, g2pk = ke_model.generate_key()

        _params = {
            "g1pk_11": str(g1pk[0]),
            "g1pk_12": str(g1pk[1]),
            "g2pk_11": str(g2pk[0].coeffs[0]),
            "g2pk_12": str(g2pk[0].coeffs[1]),
            "g2pk_21": str(g2pk[1].coeffs[0]),
            "g2pk_22": str(g2pk[1].coeffs[1]),
        }
        tx_hash, tx_receipt = ke_model.register_public_key(
            public_key=TKERegisterPublicKeyParams(**_params)
        )
        assert tx_hash is not None
        assert tx_receipt["from"] == user.address
        assert tx_receipt["status"] == 1

        registered_g1pk = ke_model.get_G1_public_key(user.address)
        assert registered_g1pk == [str(g1pk[0]), str(g1pk[1])]

        registered_g2pk = ke_model.get_G2_public_key(user.address)
        assert registered_g2pk == [
            str(g2pk[0].coeffs[0]),
            str(g2pk[0].coeffs[1]),
            str(g2pk[1].coeffs[0]),
            str(g2pk[1].coeffs[1]),
        ]


class TestGetG1PublicKey:
    def test_key_not_registered(self, key_exchange):
        user_A = get_eth_key()
        ke_model = TripartiteKeyExchangeContract(
            account=user_A, contract_address=key_exchange.address
        )
        with pytest.raises(KeyNotRegisteredError):
            ke_model.get_G1_public_key(user_A.address)

    def test_get_key(self, key_exchange):
        user_A = get_eth_key()
        ke_model_A = TripartiteKeyExchangeContract(
            account=user_A, contract_address=key_exchange.address
        )
        A_sk, A_g1pk, A_g2pk = ke_model_A.generate_key()

        _params = {
            "g1pk_11": str(A_g1pk[0]),
            "g1pk_12": str(A_g1pk[1]),
            "g2pk_11": str(A_g2pk[0].coeffs[0]),
            "g2pk_12": str(A_g2pk[0].coeffs[1]),
            "g2pk_21": str(A_g2pk[1].coeffs[0]),
            "g2pk_22": str(A_g2pk[1].coeffs[1]),
        }
        ke_model_A.register_public_key(public_key=TKERegisterPublicKeyParams(**_params))

        g1pk = ke_model_A.get_G1_public_key(user_A.address)
        assert g1pk[0] == str(A_g1pk[0])
        assert g1pk[1] == str(A_g1pk[1])


class TestGetG2PublicKey:
    def test_key_not_registered(self, key_exchange):
        user_A = get_eth_key()
        ke_model = TripartiteKeyExchangeContract(
            account=user_A, contract_address=key_exchange.address
        )
        with pytest.raises(KeyNotRegisteredError):
            ke_model.get_G2_public_key(user_A.address)

    def test_get_key(self, key_exchange):
        user_A = get_eth_key()
        ke_model_A = TripartiteKeyExchangeContract(
            account=user_A, contract_address=key_exchange.address
        )
        A_sk, A_g1pk, A_g2pk = ke_model_A.generate_key()

        _params = {
            "g1pk_11": str(A_g1pk[0]),
            "g1pk_12": str(A_g1pk[1]),
            "g2pk_11": str(A_g2pk[0].coeffs[0]),
            "g2pk_12": str(A_g2pk[0].coeffs[1]),
            "g2pk_21": str(A_g2pk[1].coeffs[0]),
            "g2pk_22": str(A_g2pk[1].coeffs[1]),
        }
        ke_model_A.register_public_key(public_key=TKERegisterPublicKeyParams(**_params))

        g2pk = ke_model_A.get_G2_public_key(user_A.address)
        assert g2pk[0] == str(A_g2pk[0].coeffs[0])
        assert g2pk[1] == str(A_g2pk[0].coeffs[1])
        assert g2pk[2] == str(A_g2pk[1].coeffs[0])
        assert g2pk[3] == str(A_g2pk[1].coeffs[1])


class TestGenerateSharedKey:
    def test_shared_key(self, key_exchange):
        user_A = get_eth_key()
        user_B = get_eth_key()
        user_C = get_eth_key()

        # Register Alice's key
        ke_model_A = TripartiteKeyExchangeContract(
            account=user_A, contract_address=key_exchange.address
        )
        A_sk, A_g1pk, A_g2pk = ke_model_A.generate_key()

        _params = {
            "g1pk_11": str(A_g1pk[0]),
            "g1pk_12": str(A_g1pk[1]),
            "g2pk_11": str(A_g2pk[0].coeffs[0]),
            "g2pk_12": str(A_g2pk[0].coeffs[1]),
            "g2pk_21": str(A_g2pk[1].coeffs[0]),
            "g2pk_22": str(A_g2pk[1].coeffs[1]),
        }
        ke_model_A.register_public_key(public_key=TKERegisterPublicKeyParams(**_params))

        # Register Bob's public key
        ke_model_B = TripartiteKeyExchangeContract(
            account=user_B, contract_address=key_exchange.address
        )
        B_sk, B_g1pk, B_g2pk = ke_model_B.generate_key()

        _params = {
            "g1pk_11": str(B_g1pk[0]),
            "g1pk_12": str(B_g1pk[1]),
            "g2pk_11": str(B_g2pk[0].coeffs[0]),
            "g2pk_12": str(B_g2pk[0].coeffs[1]),
            "g2pk_21": str(B_g2pk[1].coeffs[0]),
            "g2pk_22": str(B_g2pk[1].coeffs[1]),
        }
        ke_model_B.register_public_key(public_key=TKERegisterPublicKeyParams(**_params))

        # Register Charlie's public key
        ke_model_C = TripartiteKeyExchangeContract(
            account=user_C, contract_address=key_exchange.address
        )
        C_sk, C_g1pk, C_g2pk = ke_model_C.generate_key()

        _params = {
            "g1pk_11": str(C_g1pk[0]),
            "g1pk_12": str(C_g1pk[1]),
            "g2pk_11": str(C_g2pk[0].coeffs[0]),
            "g2pk_12": str(C_g2pk[0].coeffs[1]),
            "g2pk_21": str(C_g2pk[1].coeffs[0]),
            "g2pk_22": str(C_g2pk[1].coeffs[1]),
        }
        ke_model_C.register_public_key(public_key=TKERegisterPublicKeyParams(**_params))

        # Generate shared key
        shared_key_A = ke_model_A.generate_shared_key(
            A_sk, user_B.address, user_C.address
        )
        shared_key_B = ke_model_B.generate_shared_key(
            B_sk, user_C.address, user_A.address
        )
        shared_key_C = ke_model_C.generate_shared_key(
            C_sk, user_A.address, user_B.address
        )

        shared_key_Ao = ke_model_A.generate_shared_key(
            A_sk, user_C.address, user_B.address
        )
        shared_key_Bo = ke_model_B.generate_shared_key(
            B_sk, user_A.address, user_C.address
        )
        shared_key_Co = ke_model_C.generate_shared_key(
            C_sk, user_B.address, user_A.address
        )

        assert (
            shared_key_A
            == shared_key_B
            == shared_key_C
            == shared_key_Ao
            == shared_key_Bo
            == shared_key_Co
        )
