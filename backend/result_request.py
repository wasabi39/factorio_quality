"""
Data model for returning the result from a simulation. 
Saved as a Pydantic class in a separate file for two reasons:
1) Makes it easier to create an API, if I ever decide to make one.
2) Even if I never create an API, it makes the code cleaner, 
more readable and helps us somewhat keep the code separated 
into a frontend and a backend.
Note: The counts are floats, because they're expected values,
which aren't necessarily integers.
"""

from pydantic import BaseModel

class ResultRequest(BaseModel):
    """
    Data model for sending the result of simulation requests from backend to frontend.
    """
    quality_1_count: float
    quality_2_count: float
    quality_3_count: float
    quality_4_count: float
    quality_5_count: float
