from fastapi import FastAPI

app = FastAPI(
    title = "Backend API español",
    description = "API ubicada en el localhost enruta por API gateway /api/productos"
)

@app.get("/salud")
def salud():
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
            {"id": 1001, "estado": "pagado"},
            {"id": 1002, "estado": "pendiente" }
        ]
    }