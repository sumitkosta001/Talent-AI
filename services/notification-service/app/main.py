from fastapi import FastAPI

app = FastAPI(
    title="TalentAI Notification Service",
    description="Microservice responsible for notification operations.",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"service": "notification-service", "status": "running"}
