from fastapi import FastAPI
import uvicorn
from backend.backend import run_simulation
from frontend.computation_request import ComputationRequest
from backend.result_request import ResultRequest

app = FastAPI()

@app.post("/simulate", response_model=ResultRequest)
def simulate(computation_request: ComputationRequest) -> ResultRequest:
    result = run_simulation(computation_request)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)