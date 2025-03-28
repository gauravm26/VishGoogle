# app-api/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

#--Import Routers--
from features.project_management.api import routes as project_routes
from features.requirement_generation.api import routes as req_gen_routes
from config.settings import settings
# TODO: Import feature routers later
# from features.project_management.api import routes as project_routes


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json" # Standard OpenAPI endpoint
)

# Configure CORS (Cross-Origin Resource Sharing)
# Adjust origins as needed for your frontend URL in development/production

origins = [str(origin) for origin in settings.BACKEND_CORS_ORIGINS]
if "*" in origins: # Allow all origins if "*" is present
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
     app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.get("/ping", tags=["Health"])
async def ping():
    """Basic health check endpoint."""
    return {"message": "pong"}

@app.get(settings.API_V1_STR, include_in_schema=False)
async def api_root_redirect():
    """Redirect from /api/v1 to /docs for API documentation."""
    return RedirectResponse(url="/docs")

# TODO: Include feature routers
app.include_router(project_routes.router, prefix=settings.API_V1_STR)
app.include_router(req_gen_routes.router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    # This is for debugging locally if you run main.py directly
    # Production runs use 'uvicorn app.main:app --reload' from the app-api directory
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.BACKEND_PORT)
