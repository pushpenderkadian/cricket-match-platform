from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.routes import matches, scorecards
from backend.routes import sockets
from backend.scheduler import start_scheduler
import uvicorn
app = FastAPI()

# Include API routes
app.include_router(matches.router)
app.include_router(scorecards.router)
app.include_router(sockets.router)
start_scheduler()



# Serve frontend
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
app.mount("/", StaticFiles(directory="frontend/templates", html=True), name="frontend")

if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=5002)