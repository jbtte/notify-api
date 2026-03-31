import os
import httpx
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
API_TOKEN = os.environ["API_TOKEN"]
DOCS_ENABLED = os.getenv("DOCS_ENABLED", "false").lower() == "true"

TELEGRAM_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title="notify-api",
    docs_url="/docs" if DOCS_ENABLED else None,
    redoc_url="/redoc" if DOCS_ENABLED else None,
    openapi_url="/openapi.json" if DOCS_ENABLED else None,
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

bearer = HTTPBearer()


class NotifyRequest(BaseModel):
    project: str
    message: str
    emoji: str = "🔔"


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    if credentials.credentials != API_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


@app.get("/health", status_code=200, include_in_schema=False)
@app.head("/health", status_code=200, include_in_schema=False)
def health():
    return {"status": "ok"}


@app.post("/send", status_code=204, dependencies=[Depends(verify_token)])
@limiter.limit("10/minute")
async def send(request: Request, body: NotifyRequest):
    text = f"[{body.emoji} {body.project}]\n{body.message}"
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            TELEGRAM_URL,
            json={"chat_id": TELEGRAM_CHAT_ID, "text": text},
            timeout=10,
        )
    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail=f"Telegram error: {resp.text}")
