import os

WEB3_HTTP_PROVIDER = os.environ.get("WEB3_HTTP_PROVIDER") or "http://localhost:8545"
WEB3_REQUEST_RETRY_COUNT = int(os.environ.get("WEB3_REQUEST_RETRY_COUNT") or 3)
WEB3_REQUEST_WAIT_TIME = int(os.environ.get("WEB3_REQUEST_WAIT_TIME") or 3)
CHAIN_ID = int(os.environ.get("CHAIN_ID") or 2017)
TX_GAS_LIMIT = int(os.environ.get("TX_GAS_LIMIT") or 6000000)
