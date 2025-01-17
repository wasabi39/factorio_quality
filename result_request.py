"""
Data model for returning the result from a simulation. 
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
