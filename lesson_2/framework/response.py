from dataclasses import dataclass


@dataclass
class Response:
    status: str
    body: str
