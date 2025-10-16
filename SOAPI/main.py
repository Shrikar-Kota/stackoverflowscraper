from fastapi import FastAPI
from api.apicaller import router as apicallerrouter

app = FastAPI(title="StackOverflow Secure QA API")

# Include route modules
app.include_router(apicallerrouter, prefix="/stackoverflow", tags=["StackOverflow"])

@app.get("/")
def root():
    return {"message": "StackOverflow Secure QA API is running 🚀"}