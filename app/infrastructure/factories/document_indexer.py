import os
import uuid
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from sentence_transformers import SentenceTransformer
from typing import List
import fitz  # PyMuPDF
from pathlib import Path

# -------------------- Cargar variables de entorno --------------------
load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_COLLECTION_NAME = os.getenv("QDRANT_COLLECTION_NAME")

# Validar que no falte ninguna variable
if not QDRANT_URL or not QDRANT_API_KEY or not QDRANT_COLLECTION_NAME:
    raise ValueError("❌ Faltan variables de entorno requeridas. Verifica tu archivo .env.")

# -------------------- Clase Indexador --------------------
class DocumentIndexer:
    def __init__(self, url: str, collection_name: str, api_key: str):
        self.client = QdrantClient(
            url=url,
            api_key=api_key
        )
        self.collection_name = collection_name
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        self._asegurar_coleccion()

    def _asegurar_coleccion(self):
        """Crea la colección si no existe en Qdrant."""
        collections = self.client.get_collections().collections
        nombres = [c.name for c in collections]

        if self.collection_name not in nombres:
            print(f"⚠️ Colección '{self.collection_name}' no existe. Creando nueva colección...")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.model.get_sentence_embedding_dimension() or 384,
                    distance=Distance.COSINE
                )
            )
            print("✅ Colección creada correctamente.")

    def insert_documents(self, documents: List[str], metadatos: List[dict] = None):  # type: ignore
        points = []
        for i, doc in enumerate(documents):
            embedding = self.model.encode(doc).tolist()
            payload = {"text": doc}
            if metadatos and i < len(metadatos):
                payload.update(metadatos[i])
            points.append({
                'id': str(uuid.uuid4()),  # UUID válido
                'vector': embedding,
                'payload': payload
            })
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        return "Documentos indexados exitosamente"

# -------------------- Funciones auxiliares --------------------
def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    with fitz.open(pdf_path) as doc:  # type: ignore
        for page in doc:
            text += page.get_text()
    return text

def dividir_texto(texto: str, tamaño_fragmento: int = 500, superposicion: int = 50) -> List[str]:
    fragmentos = []
    inicio = 0
    longitud = len(texto)
    while inicio < longitud:
        fin = min(inicio + tamaño_fragmento, longitud)
        fragmentos.append(texto[inicio:fin])
        inicio += tamaño_fragmento - superposicion
    return fragmentos

def procesar_y_indexar_pdfs(rutas_pdf: List[str], indexador: DocumentIndexer):
    todos_los_fragmentos = []
    metadatos = []
    for ruta in rutas_pdf:
        print(f"📄 Procesando: {ruta}")
        texto = extract_text_from_pdf(ruta)
        fragmentos = dividir_texto(texto)
        todos_los_fragmentos.extend(fragmentos)
        metadatos.extend([{"source_pdf": os.path.basename(ruta)}] * len(fragmentos))
    respuesta = indexador.insert_documents(todos_los_fragmentos, metadatos)
    print("✅", respuesta)

# -------------------- Ejecución --------------------
if __name__ == "__main__":
    indexador = DocumentIndexer(
        url=QDRANT_URL,
        collection_name=QDRANT_COLLECTION_NAME,
        api_key=QDRANT_API_KEY
    )

    CURRENT_DIR = Path(__file__).resolve().parent  
    PDF_DIR = CURRENT_DIR.parent / "qdrant"       

    archivos_pdf = [
        str(PDF_DIR / "archivo1.pdf"),
        str(PDF_DIR / "archivo2.pdf")
    ]
    procesar_y_indexar_pdfs(archivos_pdf, indexador)
