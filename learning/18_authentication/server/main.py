from fastapi import FastAPI, HTTPException, Query, Depends, Security, status
from fastapi.security import APIKeyHeader # Import APIKeyHeader
from pydantic import BaseModel
from typing import Optional
import random
from datetime import datetime

# --- API Key Configuration ---
# Define your API key(s). In a real app, these would come from environment variables
# or a secure configuration system, not hardcoded!
API_KEY = "your-secret-fastapi-key" # <<< IMPORTANT: Change this!
API_KEY_NAME = "X-API-Key" # The name of the header where the API key will be sent

# Create an instance of APIKeyHeader. This tells FastAPI to look for a header
# named "X-API-Key" for authentication.
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# Dependency function to validate the API key
async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
        headers={"WWW-Authenticate": "X-API-Key"},
    )
# --- End API Key Configuration ---


# Initialize FastAPI app
app = FastAPI(
    title="Simple Pet Store API (Mock)",
    version="1.0.1",
    description="An API to manage pets in a store, using mock responses.",
    servers=[{"url": "http://localhost:8080"}]
)


# Global storage for pets (in-memory for demo purposes)
pets_db = []

# Pydantic models
class Pet(BaseModel):
    name: str
    tag: Optional[str] = None

class PetResponse(BaseModel):
    id: int
    name: str
    tag: Optional[str] = None
    status: str
    created_at: str

# Initialize with some sample pets
def initialize_sample_pets():
    """Initialize the pets database with sample data."""
    sample_pets = [
        {"id": 1, "name": "Buddy", "tag": "dog", "status": "available", "created_at": "2024-01-15T10:30:00Z"},
        {"id": 2, "name": "Whiskers", "tag": "cat", "status": "available", "created_at": "2024-01-16T14:20:00Z"},
        {"id": 3, "name": "Polly", "tag": "parrot", "status": "sold", "created_at": "2024-01-10T09:15:00Z"},
        {"id": 4, "name": "Goldie", "tag": "fish", "status": "pending", "created_at": "2024-01-20T16:45:00Z"},
        {"id": 5, "name": "Rex", "tag": "dog", "status": "available", "created_at": "2024-01-18T11:00:00Z"},
    ]
    pets_db.extend(sample_pets)

# Initialize sample data on startup
@app.on_event("startup")
async def startup_event():
    """Initialize sample pets on application startup."""
    initialize_sample_pets()

@app.get("/get", response_model=dict, dependencies=[Depends(get_api_key)])
async def list_pets(
    limit: Optional[int] = Query(None, description="Maximum number of pets to return"),
    status: Optional[str] = Query(None, description="Filter pets by status"),
    petId: Optional[int] = Query(None, description="Get specific pet by ID")
):
    """
    List all pets or get specific pet by ID (Simulated).
    
    Simulates returning a list of pets or specific pet info. Uses mock data instead of httpbin.
    """
    # If petId is provided, return specific pet
    if petId is not None:
        pet = next((p for p in pets_db if p["id"] == petId), None)
        
        if not pet:
            raise HTTPException(status_code=404, detail="Pet not found")
        
        # Return mock response similar to httpbin format for specific pet
        return {
            "args": {
                "petId": str(petId)
            },
            "headers": {
                "Accept": "application/json",
                "User-Agent": "FastAPI-PetStore/1.0.1"
            },
            "origin": "127.0.0.1",
            "url": f"http://localhost:8000/get?petId={petId}",
            "pet": pet
        }
    
    # Otherwise, return list of pets
    filtered_pets = pets_db.copy()
    
    # Filter by status if provided
    if status:
        if status not in ["available", "pending", "sold"]:
            raise HTTPException(status_code=400, detail="Invalid status. Must be 'available', 'pending', or 'sold'")
        filtered_pets = [pet for pet in filtered_pets if pet["status"] == status]
    
    # Apply limit if provided
    if limit and limit > 0:
        filtered_pets = filtered_pets[:limit]
    
    # Return mock response similar to httpbin format
    return {
        "args": {
            "limit": str(limit) if limit else None,
            "status": status
        },
        "headers": {
            "Accept": "application/json",
            "User-Agent": "FastAPI-PetStore/1.0.1"
        },
        "origin": "127.0.0.1",
        "url": "http://localhost:8000/get",
        "pets": filtered_pets,
        "total_count": len(filtered_pets)
    }

@app.post("/post", response_model=dict, status_code=201, dependencies=[Depends(get_api_key)])
async def create_pet(pet: Pet):
    """
    Create a pet (Simulated).
    
    Simulates adding a new pet. Uses mock data instead of httpbin.
    """
    # Generate a new pet ID
    new_id = max([pet["id"] for pet in pets_db], default=0) + 1
    
    # Create new pet
    new_pet = {
        "id": new_id,
        "name": pet.name,
        "tag": pet.tag,
        "status": random.choice(["available", "pending"]),
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    
    # Add to database
    pets_db.append(new_pet)
    
    # Return mock response similar to httpbin format
    return {
        "args": {},
        "data": pet.dict(),
        "files": {},
        "form": {},
        "headers": {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "FastAPI-PetStore/1.0.1"
        },
        "json": pet.dict(),
        "method": "POST",
        "origin": "127.0.0.1",
        "url": "http://localhost:8000/post",
        "created_pet": new_pet
    }

# Additional endpoint for health check
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# Additional endpoint to view all pets (for debugging)
@app.get("/pets")
async def get_all_pets():
    """Get all pets in the database (for debugging purposes)."""
    return {"pets": pets_db, "count": len(pets_db)} 