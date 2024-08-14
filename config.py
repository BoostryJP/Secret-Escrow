import os

WEB3_HTTP_PROVIDER = os.environ.get("WEB3_HTTP_PROVIDER") or "http://localhost:8545"
WEB3_REQUEST_RETRY_COUNT = (
    int(os.environ.get("WEB3_REQUEST_RETRY_COUNT"))
    if os.environ.get("WEB3_REQUEST_RETRY_COUNT")
    else 3
)
WEB3_REQUEST_WAIT_TIME = (
    int(os.environ.get("WEB3_REQUEST_WAIT_TIME"))
    if os.environ.get("WEB3_REQUEST_WAIT_TIME")
    else 3
)

CHAIN_ID = int(os.environ.get("CHAIN_ID")) if os.environ.get("CHAIN_ID") else 2017

TX_GAS_LIMIT = (
    int(os.environ.get("TX_GAS_LIMIT")) if os.environ.get("TX_GAS_LIMIT") else 6000000
)
