from datetime import datetime, timedelta, timezone
import os
import secrets

from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel

app = FastAPI(
    title="Authentication Service",
    description="Servicio simple de autenticación y emisión de tokens"
)

USERS = {
    "ana": {
        "password": "1234",
        "user_id": "USR-001",
        "roles": ["user"]
    },
    "pedro": {
        "password": "5678",
        "user_id": "USR-002",
        "roles": ["user"]
    },
    "ernesto": {
        "password": "admin123",
        "user_id": "USR-003",
        "roles": ["user","admin"]
    },        
}

SESSIONS = {}

TOKEN_LIFETIME_MINUTES = 15

AUTH_INTROSPECTION_SECRET = os.getenv(
    "AUTH_INTROSPECTION_SECRET",
    "demo-instrospection-secret" # gateway-auth-secret-789
)

class LoginRequest(BaseModel):
    username: str
    password: str

class IntrospectionRequest(BaseModel):
    token: str

@app.post("/login")
def login(request: LoginRequest,
    x_gateway_auth_secret: str = Header(default="")):
    if not secrets.compare_digest(
        x_gateway_auth_secret,
        AUTH_INTROSPECTION_SECRET
    ): 
        raise HTTPException(
            status_code=403,
            detail="Gateway no autorizado"
        )    
    user = USERS.get(request.username)
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Usuario incorrecto"
        )
    if user["password"] != request.password:
        raise HTTPException(
            status_code=401,
            detail="Credenciales incorrectas"
        )
    access_token = secrets.token_urlsafe(32)
    expiration = (datetime.now(timezone.utc) + timedelta(minutes=TOKEN_LIFETIME_MINUTES))
    SESSIONS[access_token] = {
        "user_id": user["user_id"],
        "username": request.username,
        "roles": user["roles"],
        "expires_at": expiration
    }
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": TOKEN_LIFETIME_MINUTES*60
    }

@app.post("/introspect")
def introspect(
    request: IntrospectionRequest,
    x_gateway_auth_secret: str = Header(default="")
):
    if not secrets.compare_digest(
        x_gateway_auth_secret,
        AUTH_INTROSPECTION_SECRET
    ): 
        raise HTTPException(
            status_code=403,
            detail="Gateway no autorizado"
        )
    session = SESSIONS.get(request.token)
    if session is None:
        return {
            "active": False
        }
    if (datetime.now(timezone.utc) > session["expires_at"]):
        SESSIONS.pop(request.token, None)
        return {
            "active": False
        }
    return {
        "active": True,
        "user_id": session["user_id"],
        "username": session["username"],
        "roles": session["roles"],
        "expires_at": session["expires_at"].isoformat()
    }
@app.post("/logout")
def logout(
    request: IntrospectionRequest,
    x_gateway_auth_secret: str = Header(default="")
): 
    if not secrets.compare_digest(
        x_gateway_auth_secret,
        AUTH_INTROSPECTION_SECRET
    ): 
        raise HTTPException(
            status_code=403,
            detail="Gateway no autorizado"
        )
    SESSIONS.pop(request.token, None)
    return {
        "message": "Sesión finalizada"
    }
@app.get("/health")
def health(x_gateway_auth_secret: str = Header(default="")):
    if not secrets.compare_digest(
        x_gateway_auth_secret,
        AUTH_INTROSPECTION_SECRET
    ): 
        raise HTTPException(
            status_code=403,
            detail="Gateway no autorizado"
        )    
    return {
        "status": "OK",
        "service": "Authentication service"
    }