from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base
import datetime

# This is the base class all our database tables will inherit from
Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(String, primary_key=True, index=True)
    source = Column(String) # e.g., 'linkedin', 'naukri'
    title = Column(String)
    company = Column(String)
    raw_text = Column(String) # The massive wall of text from the scraper
    scraped_at = Column(DateTime, default=datetime.datetime.utcnow)


#this holds the LLM output....
class ParsedJDModel(Base):
    __tablename__ = "parsed_jds"
    
    #ForeignKey - this links it directly to the Job table
    job_id = Column(String, ForeignKey("jobs.id"), primary_key=True)
    
    #JSONB to save list of strings directly into Postgres
    required_skills = Column(JSONB)
    experience_years = Column(Integer, nullable=True)
    role_level = Column(String, nullable=True)

