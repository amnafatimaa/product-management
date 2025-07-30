from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import products

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Product Management API", version="1.0.0")

# Configure CORS - Allow all origins during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(products.router, prefix="/api", tags=["products"])

@app.get("/")
async def root():
    return {"message": "Product Management API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)