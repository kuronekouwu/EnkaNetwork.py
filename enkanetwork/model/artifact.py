from pydantic import BaseModel, Field
from typing import List

class ArtifactInfo(BaseModel):
    level: int
    mainPropId: int
    appendPropIdList: List[int]

class Artifacts(BaseModel):
    id: int = Field(0, alias="itemId")
    data: ArtifactInfo = Field({}, alias="reliquary")