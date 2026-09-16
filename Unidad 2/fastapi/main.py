from typing import List, Optional, Dict
from itertools import count

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from contextlib import asynccontextmanager

#Configuracion BD mongodb
MONGODB_URI = "mongodb://localhost:27017"
DB_NAME = "bdunab2"
COLL_NAME = "items"

client: AsyncIOMotorClient | None = None
db = None
coll = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global client, db, coll
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DB_NAME]
    coll = db[COLL_NAME]
    yield
    client.close()

app = FastAPI(title="FastAPI 8479", version="1.0.0", lifespan=lifespan)

class ItemIn(BaseModel):
    nombre: str = Field(min_length=1, description="Nombre del Producto")
    precio: float = Field(gt=0, descripcion="Precio > 0")
    tags: List[str] = Field(default_factory=list)
    activo: bool = True

class Item(BaseModel):
    nombre: str = Field(min_length=1, description="Nombre del Producto")
    precio: float = Field(gt=0, descripcion="Precio > 0")
    tags: List[str] = Field(default_factory=list)
    activo: bool = True

class ItemOut(Item):
    id: str

def doc_to_itemout(doc) -> ItemOut:
    return ItemOut(
        id=str(doc["_id"]),
        nombre=doc["nombre"],
        precio=doc["precio"],
        tags=doc.get("tags", []),
        activo=doc.get("activo", True)
    )

# EndPoints
@app.get("/health", tags=["sistema"])
def health():
    return {"status":"ok"}

@app.get("/items", response_model=List[ItemOut])
async def listar_items(
    q: Optional[str] = Query(None, description="Filtro por nombre que contenga q"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
):
    query = {}
    if q:
        query["nombre"] = {"$regex": q, "$options":"i"}
    cursor = coll.find(query).skip(skip).limit(limit)
    items: list[ItemOut] = []
    async for doc in cursor:
        items.append(doc_to_itemout(doc))
    return items

@app.post("/items", response_model=ItemOut, status_code=201, tags=["items"])
async def crear_item(item: ItemIn):
    res = await coll.insert_one(item.model_dump())
    doc = await coll.find_one({"_id": res.inserted_id})
    return doc_to_itemout(doc)

# localhost:8098/items/2
@app.get("/items/{item_id}", response_model=ItemOut, status_code=201)
async def obtener_item(item_id: str):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(400, "id invalido")
    doc = await coll.find_one({"_id": ObjectId(item_id)})
    if not doc:
        raise HTTPException(404, "Item no encontrado")
    return doc_to_itemout(doc)

@app.put("/items/{item_id}", response_model=ItemOut)
async def actualizar_item(item_id: str, item: ItemIn):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(400, "id invalido")
    res = await coll.update_one(
        {"_id": ObjectId(item_id)},
        {"$set": item.model_dump()}
    )
    if res.matched_count == 0:
        raise HTTPException(404, "Item no encontrado")
    doc = await coll.find_one({"_id": ObjectId(item_id)})
    return doc_to_itemout(doc)

@app.delete("/items/{item_id}", status_code=204, tags=["items"])
async def eliminar_item(item_id: str):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(400, "id invalido")
    res = await coll.delete_one({"_id": ObjectId(item_id)})
    if res.deleted_count == 0:
        raise HTTPException(404, "Item no encontrado")
    return None