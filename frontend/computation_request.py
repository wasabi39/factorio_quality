"""
Data model for calculations. 
Saved as a Pydantic class in a separate file for two reasons:
1) Makes it easier to create an API, if I ever decide to make one.
2) Even if I never create an API, it makes the code cleaner, 
more readable and helps us somewhat keep the code separated 
into a frontend and a backend.
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
