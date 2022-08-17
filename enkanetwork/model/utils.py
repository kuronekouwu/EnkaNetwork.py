from pydantic import BaseModel
from typing import Any

from ..utils import create_ui_path

class IconAsset(BaseModel):
    filename: str = ""
    url: str = ""
    
    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

        self.url = create_ui_path(self.filename)
