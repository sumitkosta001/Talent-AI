from fastapi import FastAPI

app = FastAPI(
    title="TalentAI Recommendation Service",
    description="Microservice responsible for recommendation operations.",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"service": "recommendation-service", "status": "running"}
