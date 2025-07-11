from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from typing import List
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
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Usamos un modelo pre-entrenado para generar embeddings
    
    def search(self, query: str, top_k: int = 5) -> List[str]:
        """
        Realiza una búsqueda en Qdrant para obtener los documentos más relevantes.
        
        Args:
        - query (str): La consulta del usuario.
        - top_k (int): El número de resultados más relevantes a devolver (por defecto 5).
        
        Returns:
        - List[str]: Lista con los textos de los resultados encontrados.
        """
        # Convertir la consulta a un embedding
        embedding = self.model.encode(query).tolist()
        
        # Realizar la búsqueda en Qdrant
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=embedding,
            limit=top_k  # Limitar los resultados a `top_k`
        )
        
        # Extraer los textos de los resultados, asegurándonos de que result.payload no sea None
        return [result.payload['text'] for result in results if result.payload and 'text' in result.payload]
