from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versionizer import Versionizer, api_version

from app.cloud_functions.routes import router as s3_router

# Import routes
from app.user.routes import router as user_router
from app.utils.responses import success_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@api_version(1)
@app.get("/")
async def health_check():
    return success_response("Hello World!")

# Include route in your app
app.include_router(user_router)
app.include_router(s3_router)


versions = Versionizer(
    app=app,
    prefix_format='/v1',
    semantic_version_format='1',
    latest_prefix='/latest',
    sort_routes=True
).versionize()
