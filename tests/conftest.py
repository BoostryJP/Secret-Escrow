from typing import Any

import pytest
from pydantic import BaseModel, ConfigDict


class Users(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    admin: Any
    buyer: Any
    seller: Any
    agent: Any


@pytest.fixture()
def users(accounts) -> Users:
    admin = accounts[0]
    buyer = accounts[1]
    seller = accounts[2]
    agent = accounts[3]
    return Users(admin=admin, buyer=buyer, seller=seller, agent=agent)


@pytest.fixture()
def st_dvp_storage(project, users):
    return project.DVPStorage.deploy(sender=users.admin)


@pytest.fixture()
def st_dvp(project, users, st_dvp_storage):
    st_dvp = project.IbetSecurityTokenDVP.deploy(
        st_dvp_storage.address, sender=users.admin
    )
    st_dvp_storage.upgradeVersion(st_dvp.address, sender=users.admin)
    return st_dvp


@pytest.fixture()
def key_exchange(project, users):
    return project.TripartiteKeyExchange.deploy(sender=users.admin)
