import sys
import threading
from typing import Any

from eth_typing import URI
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.types import RPCEndpoint, RPCResponse

from config import WEB3_HTTP_PROVIDER

thread_local = threading.local()


class Web3Wrapper:
    def __init__(self):
        if "pytest" not in sys.modules:
            FailOverHTTPProvider.set_fail_over_mode(True)

    @property
    def eth(self):
        web3 = self._get_web3()
        return web3.eth

    @property
    def geth(self):
        web3 = self._get_web3()
        return web3.geth

    @property
    def net(self):
        web3 = self._get_web3()
        return web3.net

    @staticmethod
    def _get_web3() -> Web3:
        # Get web3 for each thread because make to FailOverHTTPProvider thread-safe
        try:
            web3 = thread_local.web3
        except AttributeError:
            web3 = Web3(FailOverHTTPProvider())
            web3.middleware_onion.inject(geth_poa_middleware, layer=0)
            thread_local.web3 = web3

        return web3


class FailOverHTTPProvider(Web3.HTTPProvider):
    fail_over_mode = False  # If False, use only the default(primary) provider

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.endpoint_uri = None

    def make_request(self, method: RPCEndpoint, params: Any) -> RPCResponse:
        self.endpoint_uri = URI(WEB3_HTTP_PROVIDER)
        return super().make_request(method, params)

    @staticmethod
    def set_fail_over_mode(use_fail_over: bool):
        FailOverHTTPProvider.fail_over_mode = use_fail_over
