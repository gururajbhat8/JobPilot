from pydantic import BaseModel, Field
from typing import List, Optional

class ParsedJD(BaseModel):
    required_skills: List[str] = Field(description="Must have a skills explicitly mentioned")
    nice_to_have_skill: List[str] = Field(description="Optional or preferred skills")
    experience_years: Optional[int] = Field(None, description="required year of experience.")
    role_level: Optional[str] = Field(None, description="Eg: Junior, senior, staff")
    tech_stack: List[str] = Field(description="All the tools, Language and framework mentioned")
    location: Optional[str] = Field(None, description="City, state or Remote")
    salary_range: Optional[str] = Field(None, description="Exctracted Salary if present")


class MatchResult(BaseModel):
    score: float = Field(description="Match score between 0.0 and 1.0")
    matched_skills: List[str] = Field(description="Skills present in both JD and Resume")
    missing_skills: List[str] = Field(description="Skills required from the JD but missing from Resume")
    evidence_chunks: List[str] = Field(description="Quotes from the resume supporting the match")

