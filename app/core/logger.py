"""Модуль конфигурации логирования."""

from typing import Any, Final

# Константы для ключей конфигурации
KEY_HANDLERS: Final[str] = 'handlers'
KEY_LEVEL: Final[str] = 'level'
KEY_FORMATTER: Final[str] = 'formatter'
KEY_CLASS: Final[str] = 'class'
KEY_FORMAT: Final[str] = 'format'
KEY_FMT: Final[str] = 'fmt'
KEY_STYLE: Final[str] = 'style'
KEY_STREAM: Final[str] = 'stream'
KEY_USE_COLORS: Final[str] = 'use_colors'
KEY_PROPAGATE: Final[str] = 'propagate'

# Константы для значений
STREAM_STDOUT: Final[str] = 'ext://sys.stdout'
LEVEL_DEBUG: Final[str] = 'DEBUG'
LEVEL_INFO: Final[str] = 'INFO'
CLASS_STREAM_HANDLER: Final[str] = 'logging.StreamHandler'
DEFAULT_FORMATTER: Final[str] = 'uvicorn.logging.DefaultFormatter'
ACCESS_FORMATTER: Final[str] = 'uvicorn.logging.AccessFormatter'

# Имена форматтеров и обработчиков
FORMATTER_VERBOSE: Final[str] = 'verbose'
FORMATTER_DEFAULT: Final[str] = 'default'
FORMATTER_ACCESS: Final[str] = 'access'
HANDLER_CONSOLE: Final[str] = 'console'

# Форматы сообщений
FORMAT_MAIN: Final[str] = '{asctime} - {name} - {levelname} - {message}'
FORMAT_SIMPLE: Final[str] = '{levelprefix} {message}'
FORMAT_ACCESS: Final[str] = "{levelprefix} {client_addr} - '{request_line}' {status_code}"

# Коллекции
DEFAULT_HANDLERS: Final[tuple[str, ...]] = (HANDLER_CONSOLE,)

LOGGING: Final[dict[str, Any]] = {  # noqa: WPS407
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        FORMATTER_VERBOSE: {
            KEY_FORMAT: FORMAT_MAIN,
            KEY_STYLE: '{',
        },
        FORMATTER_DEFAULT: {
            '()': DEFAULT_FORMATTER,
            KEY_FMT: FORMAT_SIMPLE,
            KEY_STYLE: '{',
            KEY_USE_COLORS: None,
        },
        FORMATTER_ACCESS: {
            '()': ACCESS_FORMATTER,
            KEY_FMT: FORMAT_ACCESS,
            KEY_STYLE: '{',
        },
    },
    'handlers': {
        HANDLER_CONSOLE: {
            KEY_LEVEL: LEVEL_DEBUG,
            KEY_CLASS: CLASS_STREAM_HANDLER,
            KEY_FORMATTER: FORMATTER_VERBOSE,
        },
        FORMATTER_DEFAULT: {
            KEY_FORMATTER: FORMATTER_DEFAULT,
            KEY_CLASS: CLASS_STREAM_HANDLER,
            KEY_STREAM: STREAM_STDOUT,
        },
        FORMATTER_ACCESS: {
            KEY_FORMATTER: FORMATTER_ACCESS,
            KEY_CLASS: CLASS_STREAM_HANDLER,
            KEY_STREAM: STREAM_STDOUT,
        },
    },
    'loggers': {
        '': {
            KEY_HANDLERS: DEFAULT_HANDLERS,
            KEY_LEVEL: LEVEL_INFO,
        },
        'uvicorn.error': {
            KEY_LEVEL: LEVEL_INFO,
        },
        'uvicorn.access': {
            KEY_HANDLERS: (FORMATTER_ACCESS,),
            KEY_LEVEL: LEVEL_INFO,
            KEY_PROPAGATE: False,
        },
    },
    'root': {
        KEY_LEVEL: LEVEL_INFO,
        KEY_FORMATTER: FORMATTER_VERBOSE,
        KEY_HANDLERS: DEFAULT_HANDLERS,
    },
}
