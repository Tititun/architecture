from dataclasses import dataclass


@dataclass
class Response:
    status: int
    body: str
