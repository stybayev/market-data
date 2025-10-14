from enum import StrEnum


class Action(StrEnum):
    SUBSCRIBE = 'subscribe'
    UNSUBSCRIBE = 'unsubscribe'
    SET = 'set'
