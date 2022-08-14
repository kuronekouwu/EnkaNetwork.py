from pydantic import BaseModel
from typing import Any

from ..utils import create_ui_path

class IconAsset(BaseModel):
    filename: str = ""
    url: str = ""
    
    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)

        __pydantic_self__.url = create_ui_path(__pydantic_self__.filename)
