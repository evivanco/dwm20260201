from fastapi import FastAPI

app = FastAPI(
    title="Backend API es",
    description="API ubicada y enrutada por API gateway"
)

@app.get("/health")
def health():
    return {
        "status": "OK",
        "service": "Backend API"
    }

@app.get("/productos")
def productos():
    return {
        "productos": [
            {"id": 1, "nombre": "Notebook", "precio": 900000},
            {"id": 2, "nombre": "Monitor", "precio": 250000}
        ]
    }

@app.get("/ordenes")
def ordenes():
    return {
        "ordenes": [
            {"id": 1001, "status": "paid"},
            {"id": 1002, "status": "pending"}
        ]
    }