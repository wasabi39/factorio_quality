"""
Data model for calculations. 
"""

from pydantic import BaseModel

class ComputationRequest(BaseModel):
    """
    Data model for sending simulation requests from frontend to backend.
    """
    productivity_boost_from_research: float
    machine_type: str
    quality_of_production_modules: str
    number_of_productivity_modules: int
    quality_of_quality_modules: str
    number_of_quality_modules: int
    number_of_iterations: int
    quality_1_count: int
    quality_2_count: int
    quality_3_count: int
    quality_4_count: int
