```
chatbot_project/
│
├── backend/
│   ├── app/
│   │   ├── adapters/
│   │   │   ├── http/
│   │   │   │   └── routes.py  # Rutas para manejar las peticiones HTTP
│   │   ├── application/
│   │   │   └── chatbot.py  # Lógica principal para el chatbot (orquestación de nodos)
│   │   ├── domain/
│   │   │   ├── model/
│   │   │   │   └── user.py  # Modelos de usuario (si es necesario)
│   │   ├── infrastructure/
│   │   │   ├── qdrant.py  # Conexión y manejo de Qdrant
│   │   │   ├── document_indexer.py  # Indexador para agregar documentos a Qdrant
│   │   │   ├── extract_info.py  # Funciones de extracción de datos del cliente
│   │   │   ├── langraph_orchestrator.py  # Orquestador de Langraph, configuración de nodos
│   │   ├── main.py  # Punto de entrada del backend (FastAPI)
│   │   ├── requirements.txt  # Dependencias de Python
│   │   ├── .env  # Variables de entorno (como URL de Qdrant y Google Gemini)
│   │   └── config.py  # Configuración general del proyecto
│   └── venv/  # Carpeta para el entorno virtual (será generada al crear el entorno)
└── frontend/  (si es necesario, por ejemplo, una UI en React)
    ├── public/
    ├── src/
    ├── package.json
    └── .env  # Variables de entorno para el frontend (si aplica)

```

# hola