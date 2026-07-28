from fastapi import FastAPI

app = FastAPI(
    title="TalentAI Auth Service",
    description="Microservice responsible for auth operations.",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"service": "auth-service", "status": "running"}
