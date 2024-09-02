import random
from decimal import Decimal
from typing import cast

import pytest
from model_bakery import baker
from model_bakery.recipe import Recipe

from django.conf import settings

from b2broker.billings.models import Transaction, Wallet


@pytest.fixture(scope="module")
def wallet_recipe() -> Recipe[Wallet]:
    return Recipe(
        Wallet,
        balance=Decimal(str(random.randint(1, 100))),
    )


@pytest.fixture(scope="module")
def transaction_recipe() -> Recipe[Transaction]:
    return Recipe(
        Transaction,
        amount=Decimal(str(random.randint(-10, 10))),
    )


@pytest.fixture
def wallet(wallet_recipe: Recipe[Wallet]) -> Wallet:
    return wallet_recipe.make(label="test", balance=Decimal("100"))


@pytest.fixture
def transaction(wallet: Wallet) -> Transaction:
    return baker.make(Transaction, wallet=wallet, txid="123", amount=Decimal("10"))


@pytest.fixture
def wallets(wallet_recipe: Recipe[Wallet]) -> list[Wallet]:
    return wallet_recipe.make(_quantity=cast(int, settings.DEFAULT_SMALL_PAGE_SIZE) + 1)


@pytest.fixture
def transactions(transaction_recipe: Recipe[Transaction]) -> list[Transaction]:
    return transaction_recipe.make(_quantity=cast(int, settings.DEFAULT_SMALL_PAGE_SIZE) + 1)
