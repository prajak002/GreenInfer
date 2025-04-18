from sqlalchemy import Column, Integer, String, Float, JSON, DateTime
from app.db.session import Base

class DeploymentAssessment(Base):
    __tablename__ = "deployment_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    cloud_provider = Column(String)
    raw_data = Column(JSON)
    recommendations = Column(JSON)
    energy_data = Column(JSON)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

class RecommendationImplementation(Base):
    __tablename__ = "recommendation_implementations"
    
    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer)
    recommendation_id = Column(String)
    status = Column(String)  # planned, in-progress, completed
    implemented_at = Column(DateTime)
    actual_savings = Column(JSON)