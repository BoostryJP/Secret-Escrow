from subprocess import DEVNULL
from typing import Generator

import pytest
from brownie import web3
from brownie.network.account import Account
from brownie.network.rpc import anvil as brownie_anvil_rpc
from pydantic import BaseModel, ConfigDict
from web3.middleware.geth_poa import geth_poa_middleware

web3.middleware_onion.inject(geth_poa_middleware, layer=0)

setattr(brownie_anvil_rpc, "PIPE", DEVNULL)


class Users(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    admin: Account
    buyer: Account
    seller: Account
    agent: Account


@pytest.fixture()
def users(web3, accounts) -> Generator[Users, None, None]:
    admin = accounts[0]
    buyer = accounts[1]
    seller = accounts[2]
    agent = accounts[3]
    users: Users = Users(admin=admin, buyer=buyer, seller=seller, agent=agent)
    yield users


@pytest.fixture()
def st_dvp_storage(DVPStorage, users):
    dvp_storage = users.admin.deploy(DVPStorage)
    return dvp_storage


@pytest.fixture()
def st_dvp(IbetSecurityTokenDVP, users, st_dvp_storage):
    deploy_args = [st_dvp_storage.address]
    st_dvp = users.admin.deploy(IbetSecurityTokenDVP, *deploy_args)
    st_dvp_storage.upgradeVersion.transact(st_dvp.address, {"from": users.admin})
    return st_dvp


@pytest.fixture()
def key_exchange(TripartiteKeyExchange, users):
    ke = users.admin.deploy(TripartiteKeyExchange)
    return ke
