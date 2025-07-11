from fastapi import FastAPI
from app.adapters.http.routes import router as chatbot_router  # Importa el router de routes.py

# Inicializa FastAPI
app = FastAPI(title="Chatbot Asesor")

# Agregar las rutas definidas en routes.py
app.include_router(chatbot_router)

@app.get("/")
async def read_root():
    """
    Endpoint de prueba para asegurarse de que la API está corriendo correctamente.
    """
    return {"message": "Bienvenido al Chatbot Asesor"}
