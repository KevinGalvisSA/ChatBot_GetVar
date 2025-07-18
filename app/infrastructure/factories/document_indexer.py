from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from typing import List

class DocumentIndexer:
    def __init__(self, url: str, collection_name: str):
        """
        Inicializa la conexión con Qdrant y el modelo para generar embeddings.
        
        Args:
        - url (str): URL del servidor Qdrant.
        - collection_name (str): El nombre de la colección dentro de Qdrant.
        """
        self.client = QdrantClient(url=url)
        self.collection_name = collection_name
        self.model = SentenceTransformer('all-MiniLM-L6-v2')  # Modelo pre-entrenado para generar embeddings
    
    def insert_documents(self, documents: List[str]):
        """
        Inserta documentos en Qdrant para indexarlos y hacerlos disponibles para búsquedas.
        
        Args:
        - documents (List[str]): Lista de textos de los documentos a indexar.
        
        Returns:
        - str: Mensaje de éxito si la operación se realiza correctamente.
        """
        points = []
        
        for doc in documents:
            embedding = self.model.encode(doc).tolist()  # Generar el embedding del documento
            payload = {"text": doc}  # Contenido del documento
            
            points.append({
                'id': hash(doc),  # ID único para el documento (usamos el hash del texto)
                'vector': embedding,
                'payload': payload
            })
        
        # Insertar los documentos en Qdrant
        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )
        
        return "Documentos indexados exitosamente"
