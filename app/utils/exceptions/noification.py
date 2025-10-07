"""Модуль содержит обработчики ошибок для уведомлений."""
from fastapi import status


class SmsSendingError(Exception):
    """Исключение для ошибок если пре отправке сообщения произошла ошибка."""

    def __init__(
        self,
        message: str,
        success: bool = False,
        phone_sms_blocked: bool | None = None,
        timeout_in_seconds: int | None = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> None:
        """
        Инициализация исключения если отправка прервана.

        Args:
            message: Сообщение об ошибке.
            phone_sms_blocked: Дополнительные детали ошибки.
            timeout_in_seconds: Время ожидания повторной отправки.
            success: Статус отправки сообщения.
            status_code: HTTP код статуса.
        """
        self.success = success
        self.message = message
        self.status_code = status_code
        self.timeout_in_seconds = timeout_in_seconds
        self.phone_sms_blocked = phone_sms_blocked
        super().__init__(self.message)
