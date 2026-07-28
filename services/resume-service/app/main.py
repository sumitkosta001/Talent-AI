from fastapi import FastAPI

app = FastAPI(
    title="TalentAI Resume Service",
    description="Microservice responsible for resume operations.",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"service": "resume-service", "status": "running"}
