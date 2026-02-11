from dataclasses import dataclass
from typing import Any


@dataclass
class UserRegistered:
    user: Any = None
    status: int | None = None
    message: str | None = None


@dataclass
class UserLogin:
    status: int = None
    message: str = None
    session_id: str | None = None