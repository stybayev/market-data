# BE-XXXX — Market-Data: выравнивание архитектуры под паттерны платформы

> ⚠️ Присвоить Jira-номер и переименовать файл в `BE-{номер}-market-data-conventions-alignment.md`.

**Jira:** https://investlink.atlassian.net/browse/BE-XXXX
**Ветка:** `feature/BE-XXXX/market-data-conventions-alignment` (от `subscription-manager`)
**Автор спеки:** stybayev@investlink.io
**Статус:** draft

---

## Контекст

`market-data` — будущий FastAPI-микросервис реалтайм-цен, который заберёт доставку
котировок опционов (а позже и акций) из монолита и закроет хронический флап
Polygon WS (см. инциденты 2026-06→07). Сейчас в ветке `subscription-manager`
лежит ранний прототип: командный путь `client_ws → Redis → subscription_manager`,
без доставки цен. Код рабочий по слоям, но **не соответствует паттернам платформы**
(auth/trading) и несёт копипаст-долг из auth.

Эта спека покрывает **только наведение порядка** — приведение архитектуры,
DI, конфига, тестов, тулинга и CI к стандарту auth/trading. Доставка цен,
провайдерный адаптер (Polygon/ThetaData) и cutover — **отдельные последующие
фазы** (см. `## Ограничения` и `## Приложение A`). Порядок важен: адаптер должен
строиться на чистом фундаменте, а не поверх растущего прототипа.

**Прод-статус:** ветка не смержена, на market-data никто из фронта/бэка ещё не
завязан — монолит по-прежнему отдаёт цены. Значит внешнего контракта, который
можно сломать, у сервиса пока нет; рефакторинг свободен. Единственный
контракт к сохранению на этой фазе — **внутренний** Redis-контракт команд между
`client_ws` и `subscription_manager` (см. `## Приложение B`).

## Требования

Acceptance criteria — сервис приведён к стандарту auth/trading без изменения
внешнего поведения того, что уже есть.

- [ ] **AC1 — DI на Dishka.** Самопальный dict-контейнер (`app/dependencies/registrator.py`
      + `app.dependency_overrides`) заменён на Dishka: провайдеры в
      `app/dependencies/providers/`, контейнер в `app/dependencies/container.py`,
      подключение через `setup_dishka()` (паттерн trading). WS-эндпоинт получает
      сервис через `FromDishka[...]`, а не `Depends(...)`.
- [ ] **AC2 — Settings на `pydantic_settings`.** Все `Settings`-классы переведены с
      `pydantic.v1.BaseSettings` + `class Config` на `pydantic_settings.BaseSettings`
      + `SettingsConfigDict`. Настройки декомпозированы в под-пакет `app/core/settings/`
      (паттерн trading). Env-префикс `MARKET_DATA_` и имена переменных сохранены
      байт-в-байт (см. `deploy/env/.env.example`).
- [ ] **AC3 — Redis без глобального мутабельного состояния.** Модульные глобалы
      `connection`/`pubsub_channel` в `app/db/redis.py` убраны. Redis-клиент отдаётся
      Dishka-провайдером (APP-scope, с корректным закрытием в lifespan/finally).
      Для standalone-процесса `subscription_manager` — отдельный контейнер/бутстрап
      (паттерн auth `create_amqp_container()`), т.к. у него свой жизненный цикл.
- [ ] **AC4 — Мёртвый код удалён.** Удалены: `app/db/postgres.py` (SQLAlchemy +
      fastapi-users, 0 моделей/0 миграций), неиспользуемые exception-модули
      (`auth.py`, `common_errors.py`, `database.py`, `monolith.py`, `noification.py`,
      `referral.py`, `verify.py`), `app/core/clients/`, неиспользуемые `app/utils/`
      (`backoff.py`, `http_error_handlers.py`, `messages.py` — после проверки
      транзитивных импортов), пустые `app/models/`, `app/api/v1/`, `app/core/integrations/`.
- [ ] **AC5 — pyproject почищен.** Из зависимостей удалены неиспользуемые
      (`alembic`, `sqlalchemy`, `fastapi-sqlalchemy`, `promise`, `psycopg2-binary`,
      `requests`, `boto3`, `fastapi-users`, `asyncpg`, `werkzeug`, `phonenumbers`,
      `async-fastapi-jwt-auth`, `python-jose`, `validate-email`, `ipython`,
      `polygon-api-client`). `pytest`/`pytest-asyncio` перенесены в dev-группу.
      `aiokafka` **оставить** (forward-looking). Имя пакета переименовано с
      `alpaca-fastapi` на `market-data`. `poetry.lock` пере-резолвится
      (`poetry lock --no-update`).
- [ ] **AC6 — Тесты по стандарту.** `pytest.ini` (addopts `-vv -s -p no:warnings`,
      asyncio loop scope), `tests/conftest.py` (`pytest_plugins`),
      `tests/unit/src/…` + `tests/unit/fixtures/`. Покрыты: `ClientWebsocketService`,
      `SubscriptionManagerWorker`, `RedisSubscriptionStorage`, `SubscriptionManager`.
      Внешний Redis замокан.
- [ ] **AC7 — Тулинг/линт.** `setup.cfg` ([flake8] `max-line-length=99`,
      `max-complexity=3`, wemake ignore-лист как в auth/trading),
      `.pre-commit-config.yaml` (wemake-python-styleguide + mypy). `flake8` чистый
      на всех файлах `app/`.
- [ ] **AC8 — Deploy/CI.** `Makefile` (up/down/build/restart/logs/test/lint/shell),
      `deploy/scripts/lint.sh`, `deploy/compose/docker-compose.lint.yml`,
      `deploy/dockerfiles/` (Dockerfile.lint), `.gitlab-ci.yml`
      (стадии `.pre/lint/review/test/build/deploy`), заполнен прод
      `deploy/compose/docker-compose.yml` (client-ws + subscription-manager + nginx).
- [ ] **AC9 — README актуализирован.** Убраны аспирационные разделы про
      Kafka/TimescaleDB/Prometheus, которых ещё нет; описано то, что реально есть.
- [ ] **AC10 — Инвариант контракта зафиксирован.** Целевой контракт фронта
      (монолит, `## Приложение A`) и внутренний командный контракт (`## Приложение B`)
      задокументированы в спеке как обязательный вход для фазы доставки цен.
- [ ] **AC11 — Зелёный прогон.** `pytest` зелёный, `flake8` чистый, сервис
      поднимается (`client-ws` принимает WS, `subscription-manager` слушает канал).

## API контракт

На этой фазе **новых REST/WS эндпоинтов не добавляем и существующие не меняем**
по форме. Рефакторится только внутреннее устройство. Целевой (будущий) контракт
фронта заморожен в `## Приложение A`; внутренний командный контракт —
в `## Приложение B`.

## Ограничения

**Не входит в скоуп этой фазы (отдельные спеки):**

- ❌ Доставка цен клиенту (массив polygon-хэшей, snapshot-on-connect, режимы
  poll/pubsub) — фаза «price delivery».
- ❌ Приведение WS-контракта фронта к монолиту (роуты `/ws/stocks/` + `/ws/options/`,
  поле `device_id`, формат опционных тикеров `T.O:OCC`) — фаза «price delivery».
- ❌ Провайдерный адаптер `MarketDataProvider` (Polygon/ThetaData), Theta Terminal,
  epoch-переключение, failover — фаза «provider adapter».
- ❌ Воркер цен (Polygon WS → Redis `ticker_data:*`) — фаза «price worker».
- ❌ TimescaleDB/Kafka, хранение баров — по мере надобности, не сейчас.

**Что НЕ меняем (сохраняем байт-в-байт):**

- Env-переменные и префикс `MARKET_DATA_` (`deploy/env/.env.example`).
- Внутренний Redis-контракт команд (канал `pubsub:subs:diff`, схема
  `SubscriptionCommandDTO`, ключи `subs:{user_id}`) — `## Приложение B`.
- Публичные имена процессов/сервисов в compose (`client-ws`, `subscription-manager`).

**Технические ограничения:**

- Postgres удаляем сейчас (мёртв), пересоберём с market-data-моделями в фазе
  хранения — копипаст из auth не тащим.
- Два entrypoint'а (FastAPI-app и standalone worker) имеют независимые жизненные
  циклы Redis — Dishka-контейнеры раздельные.

## Безопасность

- **Секреты** — только через env (`MARKET_DATA_*`), без хардкода. Проверить, что при
  чистке `.env.example`/CI не утёк реальный `API_KEY`/`SENTRY_DSN`.
- **PII** — цены и тикеры не PII; `user_id` — числовой ID, не логировать в связке с
  чувствительными данными. На этой фазе новых логов PII не вводим.
- **WS-аутентификация** — вне скоупа этой фазы (прототип без auth); требование
  аутентификации на WS зафиксировать для фазы price-delivery (монолит использует
  Django Channels `scope['user']` — микросервису понадобится JWT RS256 от auth,
  см. `microservice-communication`).

## Тест-кейсы

### Happy path
- `ClientWebsocketService.process_raw_message` на валидном `{request_id, action,
  tickers, user_id}` → `OutgoingAckDTO(status=ok)` и вызов `publish_command`
  с нормализованными тикерами.
- `SubscriptionManager.apply` subscribe/unsubscribe/set корректно меняет desired-set
  в storage.
- `SubscriptionManagerWorker` парсит валидный JSON из канала и применяет через manager.
- `RedisSubscriptionStorage` пишет/читает `subs:{user_id}` (Redis замокан).

### Edge cases
- Пустая/дублирующая строка тикеров → дедуп, порядок сохранён.
- Ровно `ws_max_subs_per_user` тикеров — проходит; на +1 — ошибка лимита.
- Нормализация регистра/пробелов (`' a.tsla '` → `A.TSLA`).
- Worker: `stop_event` завершает цикл без зависания.

### Error cases
- Невалидный JSON → `OutgoingAckDTO(status=error, error='invalid json')`, без падения.
- Тикер не по regex → ack с ошибкой валидации, `publish_command` не вызывается.
- Redis не инициализирован → `RedisNotInitializedError` (после DI — провайдер не
  отдаёт None).
- Worker: битый payload в канале → залогировано и пропущено, цикл живёт.

## Миграции данных

Не требуется. Схемы БД нет. Откат фазы = обычный git-revert MR (внешних побочных
эффектов у рефакторинга нет; данные в Redis — только эфемерные подписки).

## Тестирование

- [ ] Async-тесты через `pytest-asyncio`, внешний Redis замокан (fakeredis или
      подмена клиента через Dishka-override).
- [ ] Уникальные поля в фикстурах (`user_id`) — генерировать, не хардкодить.
- [ ] Никаких реальных сетевых вызовов (Redis/Polygon) в юнит-тестах.
- [ ] Не разводить монолитные test-файлы — бить по домену
      (`tests/unit/src/{services,subscription_manager}/…`).

## План работ (сгруппировано, с оценкой)

Порядок минимизирует риск: сначала чистка (S, механика), затем каркас (settings/DI),
затем тесты, затем тулинг/CI.

### 1. Структура и мёртвый код — S, механика
- 1.1 Удалить `app/db/postgres.py`.
- 1.2 Удалить неиспользуемые exceptions (7 модулей), `core/clients/`, лишние `utils/`.
- 1.3 Удалить пустые `models/`, `api/v1/`, `core/integrations/`.
- 1.4 `.idea/` — в `.gitignore`, снять с трекинга.

### 2. Config / Settings — S
- 2.1 `config.py`, `database.py`(или удалить), `gunicorn_conf.py`:
      `pydantic.v1` → `pydantic_settings`.
- 2.2 Перенести под-настройки в `app/core/settings/` (паттерн trading).

### 3. DI (Dishka) — M, аккуратно
- 3.1 `dishka` в зависимости.
- 3.2 `providers/infrastructure.py` — Redis (APP), заменяет глобалы `db/redis.py`.
- 3.3 `providers/services.py` — `ClientWebsocketService` (REQUEST).
- 3.4 `container.py` (`create_container()`); отдельный контейнер/бутстрап для worker.
- 3.5 `setup_dishka()` в `main.py`; закрытие контейнера в lifespan.
- 3.6 Снести `registrator.py`, `dependencies/main.py`; WS через `FromDishka[...]`.

### 4. Redis-модуль — M
- 4.1 `publish_subs_command` из модульной функции → инъектируемая зависимость
      (через сервис/провайдер). Сохранить канал/формат (`## Приложение B`).
- 4.2 Отдельный Redis-бутстрап для `subscription_manager/main.py`.

### 5. Тесты — M
- 5.1 `pytest.ini`, `conftest.py`, реорганизация в `tests/unit/src/…` + `fixtures/`.
- 5.2 Покрыть service/worker/storage/manager (см. `## Тест-кейсы`).

### 6. Тулинг/линт — S–M
- 6.1 `setup.cfg`, `.pre-commit-config.yaml`.
- 6.2 Чистка pyproject (AC5), переименование пакета, пере-lock.

### 7. Deploy/CI — M (завязано на инфру)
- 7.1 `lint.sh`, `docker-compose.lint.yml`, `deploy/dockerfiles/`.
- 7.2 `Makefile`.
- 7.3 `.gitlab-ci.yml` (стадии как в auth/trading).
- 7.4 Заполнить прод `docker-compose.yml`.

### 8. Docs — S
- 8.1 Актуализировать README под реальное состояние.

**Оценка:** ~1 неделя на 1 разработчика; п.7 зависит от деплой-специфики market-data
(реестр, ноды Swarm — согласовать с девопсом на предмет конфликта зависимостей
в Ansible/Terraform).

---

## Приложение A — ЗАМОРОЖЕННЫЙ контракт фронта (монолит, «точ в точ»)

> Это целевой внешний контракт для фазы price-delivery. На текущей фазе НЕ
> реализуется, но фиксируется как обязательный инвариант: сервис после cutover
> обязан отдавать фронту ровно это, чтобы клиент не заметил переезда.
> Источник: `backend/core/events/base_consumers.py`, `.../services/polygon_ws.py`,
> `.../services/fetch_polygon_data.py`.

**Роуты (Django Channels, AsyncJsonWebsocketConsumer):**
- `/ws/stocks/` → `StocksConsumer`
- `/ws/options/` → `OptionsConsumer`

**Аутентификация:** Django Channels `scope['user']` (сессия/куки). Для микросервиса
эквивалент — JWT RS256 от auth (детализировать в фазе price-delivery).

**Входящее (client → server):**
```json
{"action": "subscribe",   "tickers": "T.AAPL,Q.MSFT,T.O:AAPL260116C00200000", "user_id": "user-123", "device_id": "web"}
{"action": "unsubscribe", "tickers": "T.AAPL", "user_id": "user-123", "device_id": "web"}
{"action": "client_disconnect", "user_id": "user-123", "device_id": "web"}
```
- `tickers` — CSV. Стоки: `{T|Q|A}.SYMBOL`. Опционы: `{T|Q|A}.O:{OCC}`,
  где OCC `^[A-Z]{1,10}\d{6}[CP]\d{8}$` (напр. `AAPL260116C00200000`).
- `StocksConsumer` отбрасывает `.O`-тикеры; `OptionsConsumer` — оставляет только `.O`.
- `device_id` обязателен: tracking = `{user_id}:{device_id}` (мультидевайс).

**Исходящее (server → client):** JSON-**массив** сырых polygon-хэшей, только
изменившиеся тикеры с прошлого тика:
```json
[
  {"ev":"T","sym":"AAPL","t":"1639506000123","p":"150.25","s":"100","c":["12"],"x":"4"},
  {"ev":"Q","sym":"MSFT","t":"1639506000456","bid":"340.50","ask":"340.55","bs":"500","as":"300"},
  {"ev":"T.O","sym":"O:AAPL260116C00200000","t":"1639506000789","p":"12.50","s":"50","x":"1"}
]
```
- Trade (`ev=T`/`T.O`): `p,s,c,x`. Quote (`ev=Q`/`Q.O`): `bid,ask,bs,as`. Все значения — строки.
- Опционный `sym` префиксован `O:`.

**Ошибки:** `{"error":"<текст>"}`. Явных ack/подтверждений подписки НЕТ (успех молчаливый).

**Redis (worker → consumer) — контракт хранения:**
- Ключ: `ticker_data:{prefix}{delim}{symbol}` — опцион `ticker_data:T.O:AAPL260116C00200000`,
  сток `ticker_data:T.AAPL`.
- Тип: **HASH** (HSET) с полями = поля polygon-хэша выше. TTL = `TICKER_DATA_TTL` (72ч).
- Санитизация при записи: `bool→'true'/'false'`, `list→CSV`, `None→''`.
- Pub/sub уведомление: канал `ticker_update:ticker_data:{ticker}`, payload = timestamp `t`.

**Режимы доставки:**
- `USE_PUBSUB_MODE=false` (default) — poll каждые `SOCKET_UPDATE_PERIOD` мс (1000),
  diff по полю `t`, шлём массив изменённых.
- `USE_PUBSUB_MODE=true` — слушаем `ticker_update:*`, аккумулируем, флашим батч
  каждые `PUBSUB_THROTTLE_MS` (100).
- **Snapshot-on-connect** — при первой подписке слать текущее состояние из Redis
  (фикс «пустого экрана», инцидент 2026-06-09) — обязателен.

**Change-detection:** сравнение поля `t` (быстрый путь) или полное равенство dict;
слать только при изменении.

---

## Приложение B — ВНУТРЕННИЙ контракт команд (сохранить на этой фазе)

> Кросс-процессный контракт между `client_ws` (publisher) и `subscription_manager`
> (consumer). При рефакторинге DI/Redis сохранить байт-в-байт.

- **Канал:** `pubsub:subs:diff` (env `MARKET_DATA_REDIS_PUBSUB_CHANNEL`).
- **Сообщение** (`app/schemas/pubsub.py::SubscriptionCommandDTO`, `extra='allow'`):
```json
{"op": "subscribe", "user_id": 123, "tickers": ["A.TSLA", "Q.TQQQ"]}
```
  - `op` ∈ `Action` (`subscribe`/`unsubscribe`/`set`). Сериализация: `exclude_none=True`,
    `separators=(',',':')`.
- **Storage:** `RedisSubscriptionStorage` — Redis SET `subs:{user_id}`.
- **Лимит:** `ws_max_subs_per_user` (env, default 500).

> Примечание: формат тикеров прототипа (`^[A-Z]\.[A-Z0-9]+$`, только стоки) и
> отсутствие `device_id` — расхождение с монолитом (`## Приложение A`), устраняется
> в фазе price-delivery, НЕ здесь.

---

## Риски / заметки

1. **`publish_subs_command` — модульная функция**, импортируется в `ws/client_ws.py`.
   При переходе на Dishka станет инъектируемой; проверить, что канал/сериализация не
   поехали (`## Приложение B`).
2. **Два жизненных цикла Redis** (app + standalone worker) — раздельные контейнеры
   (паттерн auth `create_container()` / `create_amqp_container()`).
3. **Чистка pyproject** требует пере-резолва `poetry.lock` — проверить, что lock
   сходится и образ собирается.
4. **Прод `docker-compose.yml` пустой** — блокер для CI-стадии deploy; согласовать
   ноды/реестр с девопсом (и infra-конфликты в Ansible/Terraform).
5. **Фаза сознательно предшествует адаптеру/доставке цен** — чтобы провайдерный слой
   строился на чистом фундаменте.
6. **Postgres удаляется** — при будущем хранении баров собирать заново под
   market-data-модели, копипаст из auth не возвращать.
