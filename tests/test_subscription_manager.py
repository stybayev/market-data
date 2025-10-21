import pytest

from app.enums import Action
from app.subscription_manager.service import SubscriptionManager, SubscriptionStorage


class InMemoryStorage(SubscriptionStorage):
    def __init__(self) -> None:
        self._data: dict[int, list[str]] = {}

    async def add_tickers(self, user_id: int, tickers: list[str]) -> list[str]:  # noqa: D401
        state = set(self._data.get(user_id, [])) | set(tickers)
        self._data[user_id] = sorted(state)
        return self._data[user_id]

    async def remove_tickers(self, user_id: int, tickers: list[str]) -> list[str]:
        state = set(self._data.get(user_id, [])) - set(tickers)
        self._data[user_id] = sorted(state)
        return self._data[user_id]

    async def set_tickers(self, user_id: int, tickers: list[str]) -> list[str]:
        self._data[user_id] = sorted(set(tickers))
        return self._data[user_id]


@pytest.mark.asyncio
async def test_subscribe_adds_unique_tickers() -> None:
    storage = InMemoryStorage()
    manager = SubscriptionManager(storage, max_subs_per_user=5)

    state = await manager.handle(action=Action.SUBSCRIBE, user_id=1, tickers=['AAPL', 'TSLA'])
    assert state == ['AAPL', 'TSLA']

    state = await manager.handle(action=Action.SUBSCRIBE, user_id=1, tickers=['TSLA', 'MSFT'])
    assert state == ['AAPL', 'MSFT', 'TSLA']


@pytest.mark.asyncio
async def test_unsubscribe_removes_tickers() -> None:
    storage = InMemoryStorage()
    manager = SubscriptionManager(storage, max_subs_per_user=5)

    await manager.handle(action=Action.SUBSCRIBE, user_id=1, tickers=['AAPL', 'TSLA'])
    state = await manager.handle(action=Action.UNSUBSCRIBE, user_id=1, tickers=['TSLA'])

    assert state == ['AAPL']


@pytest.mark.asyncio
async def test_set_overwrites_state() -> None:
    storage = InMemoryStorage()
    manager = SubscriptionManager(storage, max_subs_per_user=5)

    await manager.handle(action=Action.SUBSCRIBE, user_id=1, tickers=['AAPL'])
    state = await manager.handle(action=Action.SET, user_id=1, tickers=['MSFT'])

    assert state == ['MSFT']


@pytest.mark.asyncio
async def test_limit_violation_raises_error() -> None:
    storage = InMemoryStorage()
    manager = SubscriptionManager(storage, max_subs_per_user=1)

    await manager.handle(action=Action.SUBSCRIBE, user_id=1, tickers=['AAPL'])

    with pytest.raises(ValueError):
        await manager.handle(action=Action.SUBSCRIBE, user_id=1, tickers=['MSFT'])

