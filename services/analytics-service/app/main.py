from fastapi import FastAPI

app = FastAPI(
    title="TalentAI Analytics Service",
    description="Microservice responsible for analytics operations.",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"service": "analytics-service", "status": "running"}
