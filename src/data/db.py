from dataclasses import dataclass


@dataclass
class InsertResult:
    success: bool
    existed: bool
    faulted: bool