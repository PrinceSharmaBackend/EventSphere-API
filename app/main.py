from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.event import router as event_router
from app.api.admin import router as admin_router
from fastapi.responses import RedirectResponse

app = FastAPI(
    title="EventSphere API",
    version="1.0.0"
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(event_router)
app.include_router(admin_router)


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")