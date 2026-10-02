import os
import secrets

from fastapi import (
    FastAPI,
    Header,
    HTTPException,
    Depends
)
app = FastAPI(
    title = "Protected Backend API ingles",
    description = "API ubicada en el localhost enruta por API gateway /api/products y /api/orders"
)

#SELINUX
INTERNAL_GATEWAY_SECRET = os.getenv(
    "INTERNAL_GATEWAY_SECRET"
)

if not INTERNAL_GATEWAY_SECRET:
    raise RuntimeError(
        "INTERNAL_GATEWAY_SECRET no está configurado"
    )

def verify_gateway(
        x_gateway_secret: str = Header(default="")
):
    valid = secrets.compare_digest(
        x_gateway_secret,
        INTERNAL_GATEWAY_SECRET
    )
    if not valid:
        raise HTTPException(
            status_code=403,
            detail="Solicitud no autorizada desde gateway"
        )


@app.get(
        "/health",
        dependencies=[Depends(verify_gateway)]
        )
def health(
    x_authenticated_client: str | None = Header(
        default=None
    )
):
    return {
        "authenticated_client": x_authenticated_client,
        "status": "OK", 
        "service": "Backend API"
    }
@app.get(
        "/products",
        dependencies=[Depends(verify_gateway)]
        )
def products(
    x_authenticated_client: str | None = Header(default=None),
    x_authenticated_user: str | None = Header(default=None),
    x_authenticated_roles: str | None = Header(default=None)
):
    return {
        "identity": {
            "client_id": x_authenticated_client,
            "username": x_authenticated_user,
            "roles": x_authenticated_roles
        },
        "products": [
            {"id": 1, "name": "Notebook", "price": 900000},
            {"id": 2, "name": "Monitor", "price": 250000}
        ]
    }
@app.get(
        "/orders",
        dependencies=[Depends(verify_gateway)]
        )
def orders(
    x_authenticated_client: str | None = Header(default=None),
    x_authenticated_user: str | None = Header(default=None),
    x_authenticated_roles: str | None = Header(default=None)  
):
    return {
        "identity": {
            "client_id": x_authenticated_client,
            "username": x_authenticated_user,
            "roles": x_authenticated_roles
        },
        "orders": [
            {"id": 1001, "status": "paid"},
            {"id": 1002, "status": "pending" }
        ]
    }