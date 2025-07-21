from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from typing import List
from app.models.context_chunk import ContextChunk  # Asegúrate de que este archivo exista
import os

class QdrantService:
    def __init__(self, url: str, collection_name: str, api_key: str):
        """
        Constructor para inicializar el cliente Qdrant y el modelo de Sentence Transformer.
        
        Args:
        - url (str): URL del servidor Qdrant.
        - collection_name (str): El nombre de la colección dentro de Qdrant.
        - api_key (str): La clave de API para acceder a Qdrant.
        """
        self.client = QdrantClient(url=url, api_key=api_key)
        self.collection_name = collection_name
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Modelo pre-entrenado para embeddings

    def search(self, query: str, top_k: int = 5) -> List[ContextChunk]:
        """
        Realiza una búsqueda en Qdrant y devuelve resultados como ContextChunk.
        
        Args:
        - query (str): La consulta del usuario.
        - top_k (int): Número de resultados a devolver.
        
        Returns:
        - List[ContextChunk]: Lista de chunks con contenido relevante.
        """
        # Convertir la consulta a un embedding
        embedding = self.model.encode(query).tolist()
        
        # Realizar la búsqueda
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=embedding,
            limit=top_k
        )
        
        # Devolver resultados como ContextChunk
        return [
            ContextChunk(text=result.payload['text'], score=result.score)
            for result in results
            if result.payload and 'text' in result.payload
        ]
