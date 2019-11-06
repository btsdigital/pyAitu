from dataclasses import dataclass


@dataclass
class ValidationRule:
    type: str
    value: str
    error: str
