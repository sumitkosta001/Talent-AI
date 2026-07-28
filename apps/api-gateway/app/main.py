from fastapi import FastAPI

app = FastAPI(
    title="TalentAI API Gateway",
    description="Routing traffic, managing authentication checking, and rate limiting.",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Welcome to TalentAI API Gateway"}
