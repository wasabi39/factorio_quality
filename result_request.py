from pydantic import BaseModel
#Data model for returning the result from a simulation. 
#Saved as a Pydantic class in a separate file for two reasons:
#1) Makes it easier to create an API, if I ever decide to make one.
#2) Even if I never create an API, it makes the code cleaner, 
#more readable and helps us somewhat keep the code separated 
#into a frontend and a backend.
class ResultRequest(BaseModel):
    quality_1_count: int
    quality_2_count: int
    quality_3_count: int
    quality_4_count: int
    quality_5_count: int