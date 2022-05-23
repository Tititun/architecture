from dataclasses import dataclass
from view import View


@dataclass
class Url:
    path: str
    view: View