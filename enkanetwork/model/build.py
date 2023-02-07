from pydantic import BaseModel

from .character import CharacterInfo

from typing import Dict, List, Any

class BuildInfo(BaseModel):
    id: int
    name: str = ''
    avatar_id: str = ''
    avatar_data: CharacterInfo
    order: int = 0
    live: bool = False
    settings: Dict[str, Any] = {}
    public: bool = True

class Builds(BaseModel):
    raw: Dict[str, List[BuildInfo]] = {}

    def __init__(self, **data: Any) -> None:
        _data = {}
        for key in data:
            _build = []
            for build in data[key]:
                _build.append(build)

            _data[key] = _build

        super().__init__(**{"raw": _data})

    def get_build_info(self, avatar_id: str, build_id: str):
        buildList = self.raw.get(str(avatar_id), None)
        if buildList is None:
            return None
        
        for buildInfo in buildList:
            if str(buildInfo.id) == build_id:
                return buildInfo

        return None

    def get_character(self, avatar_id: str):
        return self.raw.get(str(avatar_id), None)

    def get_avatar_list(self):
        return [avatar_id for avatar_id in self.raw]