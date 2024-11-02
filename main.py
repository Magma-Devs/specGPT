from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from utils.grpc import run_grpcurl


# Define the FastAPI app
app = FastAPI()

# Define the request model for receiving gRPC URL
class GrpcRequest(BaseModel):
    url: str

@app.post("/query_grpc")
async def query_grpc(request: GrpcRequest):
    try:
        # Run grpcurl with the provided URL
        description = run_grpcurl(request.url)
        return {"description": description}

    except RuntimeError as e:
        # Handle errors from grpcurl
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        # Handle any other unexpected errors
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
