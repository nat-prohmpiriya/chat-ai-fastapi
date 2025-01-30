# src/utils/result.py
from dataclasses import dataclass
from typing import Any, Optional

@dataclass
class Error:
    status: int
    message: str

@dataclass
class Result(Exception):
    ok: bool
    value: Optional[Any] = None
    error: Optional[Error] = None

def ok(value: Any = None) -> Result:
    return Result(ok=True, value=value)

def err(status: int, message: str) -> Result:
    return Result(ok=False, error=Error(status=status, message=message))