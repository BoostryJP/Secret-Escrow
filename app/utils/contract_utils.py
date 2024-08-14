import json
from typing import Tuple, Type, TypeVar

from eth_utils import to_checksum_address
from web3.contract import Contract
from web3.exceptions import (
    ABIFunctionNotFound,
    BadFunctionCallOutput,
    ContractLogicError,
    TimeExhausted,
)

from app.exceptions import SendTransactionError
from app.utils.web3_utils import Web3Wrapper
from config import CHAIN_ID, TX_GAS_LIMIT

web3 = Web3Wrapper()


class ContractUtils:
    factory_map: dict[str, Type[Contract]] = {}

    @staticmethod
    def get_contract_code(contract_name: str):
        """Get contract code

        :param contract_name: contract name
        :return: ABI, bytecode, deployedBytecode
        """
        contract_json = json.load(open(f"build/contracts/{contract_name}.json", "r"))

        if "bytecode" not in contract_json.keys():
            contract_json["bytecode"] = None
            contract_json["deployedBytecode"] = None

        return (
            contract_json["abi"],
            contract_json["bytecode"],
            contract_json["deployedBytecode"],
        )

    @staticmethod
    def deploy_contract(
        contract_name: str, args: list, deployer: str, private_key: str
    ) -> Tuple[str, dict, str]:
        """Deploy contract

        :param contract_name: contract name
        :param args: arguments given to constructor
        :param deployer: contract deployer
        :param private_key: private key
        :return: contract address, ABI, transaction hash
        """
        contract_file = f"contracts/{contract_name}.json"
        try:
            contract_json = json.load(open(contract_file, "r"))
        except FileNotFoundError as file_not_found_err:
            raise SendTransactionError(file_not_found_err)

        contract = web3.eth.contract(
            abi=contract_json["abi"],
            bytecode=contract_json["bytecode"],
            bytecode_runtime=contract_json["deployedBytecode"],
        )

        try:
            # Build transaction
            tx = contract.constructor(*args).build_transaction(
                transaction={
                    "chainId": CHAIN_ID,
                    "from": deployer,
                    "gas": TX_GAS_LIMIT,
                    "gasPrice": 0,
                }
            )
            # Send transaction
            tx_hash, tx_receipt = ContractUtils.send_transaction(
                transaction=tx, private_key=private_key
            )
        except TimeExhausted as timeout_error:
            # NOTE: Time-out occurred because sending transaction stays in pending, etc.
            raise SendTransactionError(timeout_error)
        except Exception as error:
            raise SendTransactionError(error)

        contract_address = None
        if tx_receipt is not None:
            # Check if contract address is registered from transaction receipt result.
            if "contractAddress" in tx_receipt.keys():
                contract_address = tx_receipt["contractAddress"]

        return contract_address, contract_json["abi"], tx_hash

    @classmethod
    def get_contract(cls, contract_name: str, contract_address: str):
        """Get contract

        :param contract_name: contract name
        :param contract_address: contract address
        :return: Contract
        """
        contract_factory = cls.factory_map.get(contract_name)
        if contract_factory is not None:
            return contract_factory(address=to_checksum_address(contract_address))

        contract_file = f"build/contracts/{contract_name}.json"
        contract_json = json.load(open(contract_file, "r"))
        contract_factory = web3.eth.contract(abi=contract_json["abi"])
        cls.factory_map[contract_name] = contract_factory
        return contract_factory(address=to_checksum_address(contract_address))

    T = TypeVar("T")

    @staticmethod
    def call_function(
        contract: Contract, function_name: str, args: tuple, default_returns: T = None
    ) -> T:
        """Call contract function

        :param contract: Contract
        :param function_name: Function name
        :param args: Function args
        :param default_returns: Default return when web3 exceptions are raised
        :return: Return from function or default return
        """
        try:
            _function = getattr(contract.functions, function_name)
            result = _function(*args).call()
        except (
            BadFunctionCallOutput,
            ABIFunctionNotFound,
            ContractLogicError,
        ) as web3_exception:
            if default_returns is not None:
                return default_returns
            else:
                raise web3_exception

        return result

    @staticmethod
    def send_transaction(transaction: dict, private_key: str):
        """Send transaction"""
        _tx_from = transaction["from"]

        # Get nonce
        nonce = web3.eth.get_transaction_count(_tx_from)
        transaction["nonce"] = nonce
        signed_tx = web3.eth.account.sign_transaction(
            transaction_dict=transaction, private_key=private_key
        )
        # Send Transaction
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction.hex())
        tx_receipt = web3.eth.wait_for_transaction_receipt(
            transaction_hash=tx_hash, timeout=10
        )
        if tx_receipt["status"] == 0:
            raise SendTransactionError

        return tx_hash.hex(), tx_receipt

    @staticmethod
    def get_block_by_transaction_hash(tx_hash: str):
        """Get block by transaction hash

        :param tx_hash: transaction hash
        :return: block
        """
        tx = web3.eth.get_transaction(tx_hash)
        block = web3.eth.get_block(tx["blockNumber"])
        return block
