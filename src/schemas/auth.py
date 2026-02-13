from pydantic import BaseModel


class Register(BaseModel):
    """
    Тело POST-запросов на авторизацию и регистрацию пользователя в системе

    :param username: имя пользователя
    :param password: пароль пользователя
    """

    username: str
    password: str