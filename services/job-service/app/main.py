from fastapi import FastAPI

app = FastAPI(
    title="TalentAI Job Service",
    description="Microservice responsible for job operations.",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"service": "job-service", "status": "running"}
