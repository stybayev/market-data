"""Сообщения при регистрации пользователя."""

# Сообщения сервиса
INVALID_SERVICE_TOKEN = 'Invalid service token'

# Сообщения для пользователя
USER_EMAIL_EXISTS = 'A user with this E-mail is already registered'
USER_PHONE_EXISTS = 'A user with this phone number is already registered'
USER_NOTIFICATIONS_EXISTS = 'The user already has general notification settings'
ERROR_SAVING_USER = 'Error saving user'
DATA_UNIQUENESS_ERROR = 'Data uniqueness error'
USER_NOT_FOUND = 'You entered the wrong login or password'
USER_IN_ACTIVE = 'User is not active'
BROKER_ID_EXISTS = 'A user with id={user_id} already has a brokerage account.'
USER_UPDATE_SUCCESS_MESSAGE = 'Your data has been successfully updated'

# Сообщения валидации
INVALID_PHONE = 'Invalid phone number entered'
REF_CODE_NOT_FOUND = 'Invalid promo code entered'
INVALID_EMAIL = 'Invalid email address'
EMPTY_EMAIL_FIELD = 'The email field must not be empty'
EMPTY_PHONE_NUMBER_FIELD = 'The phone_number field must not be empty'
EMPTY_PASSWORD_FIELD = 'The password field must not be empty'  # noqa: S105
PHONE_COUNTRY_NOT_FOUND = 'Failed to determine country (iso code) from phone number'
INVALID_FIELD_VALUE = 'Invalid value "{value}"'
REQUIRED_FIELDS_MISSING = 'Required fields are missing.'
ONLY_ONE_FIELD_ALLOWED = 'Only one of "like" or "user_ids" can be provided.'
REQUIRED_FIELD = 'Required field.'
INVALID_FIELD_LENGTH = 'Invalid value length. No more than 3 characters allowed.'
EMPTY_EMAIL_VERIFICATION_CODE_FIELD = 'The email_verification_code field must not be empty'
EMPTY_PHONE_VERIFICATION_CODE_FIELD = 'The phone_verification_code field must not be empty'

# HTTP клиент ошибки
HTTP_CLIENT_ERROR = 'HTTP client error'
HTTP_CLIENT_TIMEOUT_ERROR = 'Request timeout exceeded'
HTTP_CLIENT_CONNECTION_ERROR = 'Service connection error'
HTTP_CLIENT_RESPONSE_ERROR = 'Service response error'
HTTP_CLIENT_NOT_INITIALIZED = 'HTTP client not initialized'
ALPACA_CLIENT_NOT_INITIALIZED = 'ALPACA client not initialized'
STATUS_CODE_KEY = 'status_code'

# Сообщения telegram бота
TELEGRAM_MESSAGE_TEXT_REGISTRATION = 'Telegram registration message sent for user ID'  # noqa: E501

# Сообщения ошибок
ERROR_TOKEN = 'Bearer token is missing.'
ERROR_TOKEN_TYPE = 'Only Bearer token is supported.'
ERROR_TOKEN_EXPIRED = 'Invalid or expired token.'
ERROR_REFRESH_TOKEN = 'Invalid refresh token'
ERROR_ACCESS_TOKEN = 'Invalid access token'
TOKEN_IS_BLACKLISTED = 'Token is blacklisted'

# Сообщения базы
USER_WITH_ID_NOT_FOUND = 'User with ID {user_id} not found.'
MANAGER_WITH_ID_NOT_FOUND = 'Manager with ID {user_id} not found.'
ANKETA_NOT_FOUND = 'User questionnaire not found'
ANKETA_ALREADY_EXISTS = 'Questionnaire for this user already exists'

# Сообщения при верификации электронной почты и номера телефона
VERIFY_CODE_ERROR = 'Enter a 4-digit confirmation code'
EMAIL_VERIFICATION_SUCCESS = 'Congratulations! You have successfully verified your E-mail: {email}'
PHONE_VERIFICATION_SUCCESS = (
    'Congratulations! You have successfully verified your phone number: {phone_number}'
)
INCORRECT_VERIFY_CODE = 'You entered an incorrect confirmation code'
EMAIL_HAS_ALREADY_BEEN_VERIFIED = 'Email has already been verified.'
SMS_BLOCKED = (
    'Contact platform administrators by another method to verify your phone number'
)
CODE_SENT_SUCCESS_MESSAGE = 'Confirmation code successfully sent to your phone number'
PHONE_HAS_ALREADY_BEEN_VERIFIED = 'Phone has already been verified.'
USER_WITH_EMAIL_NOT_FOUND = 'User with email: {email} not found.'
USER_WITH_PHONE_NOT_FOUND = 'User with the specified phone number does not exist.'
RESEND_VERIFICATION_EMAIL_CODE_SUCCESS = (
    'Verification code was successfully resent to {email}.'
)

# Сообщения для уведомлений
NOTIFICATION_SEND_FAILED_MSG = 'Failed to send notification. Error: {error}'

# Сообщения KYC
ANKETA_DATA_FILLED = 'User: filled out the questionnaire data'
FIO_CHANGE_RESTRICTED_ERROR = (
    'Changing full name after receiving a brokerage account is allowed only once.'
)

# Сообщения BID
ACCOUNT_DELETE_REQUEST_MESSAGE = 'Account deletion request'
CREATE_ACCOUNT_DELETE_BID = 'Account deletion request created'
BID_DELETE_ACCOUNT_REQUEST_FAILED = 'Failed to create account deletion request.'

# Сообщения прав доступа
PERMISSION_DENIED_MESSAGE = 'Insufficient rights to perform the action.'
ONLY_FOR_MANAGER_OR_SUPER_ADMIN = 'Access allowed only for manager or supermanager.'

# Сообщения реферальной программы
USER_NOT_PARTNER_ERROR = 'User with ID {user_id} is not a partner.'
PARTNER_NO_REF_CODE_ERROR = 'Partner with ID {user_id} does not have a referral code.'

# Менеджеры
USER_IS_NOT_MANAGER = 'User is not a manager'
