from typing import TypedDict, Optional
from app.models.schemas import ParsedJD


class JobPipelineState(TypedDict):
    job_id : str 
    raw_text: str 
    parsed_jd: Optional[ParsedJD]

    