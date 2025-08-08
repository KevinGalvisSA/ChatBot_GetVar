
## 🌟 Nombre del Proyecto

**ChatBot - Asesorías (KAI)**

A continuación se presenta la documentación actualizada del proyecto **ChatBot - Asesorías**.

---

## 🧠 Descripción General

**KAI** es un asistente conversacional diseñado para comprender los problemas de los usuarios, realizar preguntas específicas, y ofrecer soluciones a través de automatización e inteligencia artificial. Al finalizar una sesión, sugiere una **capacitación personalizada** o la **venta de un producto funcional** para implementar la solución.

---

## ✅ Requerimientos Funcionales

1. Desarrollo de KAI utilizando LLMs (Gemini, OpenAI, DeepSeek, etc.).
2. Conversación contextual basada en historial y seguimiento de mensajes.
3. Captura y análisis de datos clave del cliente (nombre, teléfono).
4. Almacenamiento de conversaciones y datos en MySQL y Qdrant.
5. Generación de resúmenes automáticos y persistentes al finalizar el chat.
6. Presentación de soluciones adaptadas a cada caso.
7. Sugerencia de productos o capacitación como acción final.

---

## 🧰 Tecnologías Utilizadas

| Tecnología         | Rol                  | Descripción                                              |
|-------------------|----------------------|----------------------------------------------------------|
| Node.js           | Backend API          | Entorno de ejecución para TypeScript.                    |
| TypeScript        | Backend API          | Superset de JavaScript con tipado estático.              |
| Express           | Backend API          | Framework para construir APIs REST.                      |
| FastAPI           | IA / Orquestación    | Framework moderno en Python para servicios web.          |
| Python            | IA / Lógica Bot      | Lenguaje principal para orquestación del bot.            |
| Gemini            | LLM                  | Modelo de lenguaje multimodal de Google.                 |
| OpenAI            | LLM                  | Modelos de lenguaje de OpenAI (opcional/configurable).   |
| DeepSeek          | LLM                  | Modelos alternativos de lenguaje (opcional/configurable).|
| LangChain         | Orquestación         | Composición de herramientas y LLMs.                      |
| LangGraph         | Orquestación         | Flujos de nodos secuenciales para LangChain.             |
| MySQL             | Base de datos        | Almacenamiento estructurado de usuarios y chats.         |
| Qdrant            | Vector DB            | Búsquedas semánticas mediante embeddings.                |
| sentence-transformers | Embeddings        | Generación de vectores semánticos para Qdrant.           |
| PyMySQL           | Conector DB Python   | Conexión de Python a MySQL.                              |
| Uvicorn           | Servidor ASGI        | Servidor para aplicaciones FastAPI.                      |
| Socket.IO         | Comunicación         | Comunicación en tiempo real entre backend y clientes.     |
| dotenv            | Configuración        | Manejo de variables de entorno.                          |
| Otros             | Utilidades           | Logger, middlewares, scripts de prueba, etc.             |

---

## 🗂️ Estructura del Proyecto

### 🐍 Python – IA / FastAPI / LangChain

```
ChatBot_GetVar/
├─ app/
│   ├─ adapters/
│   │   └─ http/
│   │       └─ routes.py
│   ├─ application/
│   │   ├─ agent/
│   │   │   ├─ chatbot.py
│   │   │   └─ langgraph_flow.py
│   │   ├─ prompts/
│   │   │   └─ base_prompt.py
│   │   └─ tools/
│   │       ├─ tool_check_AB.py
│   │       ├─ tool_check_sent.py
│   │       ├─ tool_extractor.py
│   │       ├─ tool_gemini.py
│   │       ├─ tool_prompt.py
│   │       ├─ tool_qdrant.py
│   │       ├─ tool_save_message.py
│   │       ├─ tool_save_user.py
│   │       └─ tool_state.py
│   ├─ config/
│   │   └─ bot_regulations.py
│   ├─ configuration.py
│   ├─ domain/
│   │   └─ model/
│   │       ├─ base.py
│   │       ├─ customer.py
│   │       ├─ messageStorage.py
│   │       ├─ state.py
│   │       ├─ stateStorage.py
│   │       └─ user.py
│   ├─ infrastructure/
│   │   ├─ factories/
│   │   │   ├─ extract_info.py
│   │   │   ├─ gemini_integration.py
│   │   │   └─ qdrant.py
│   │   └─ sql/
│   │       ├─ customer_saver.py
│   │       ├─ message_saver.py
│   │       ├─ setupDB.py
│   │       └─ state_saver.py
│   ├─ main.py
│   ├─ models/
│   │   └─ context_chunk.py
│   └─ requirements.txt
├─ text_gemini.py
├─ venv/
```

### 🔷 Node.js – Backend API

```
ChatBot_GetVar/
└── backend/
    ├── package.json
    ├── tsconfig.json
    ├── db_conectionTest.ts
    ├── logs/
    └── src/
        ├── adapters/
        │   └── http/
        │       ├── controllers/
        │       │   ├── chat_controller.ts
        │       │   ├── customer_controller.ts
        │       │   ├── message_controller.ts
        │       │   ├── messageStorage_controller.ts
        │       │   └── webhook_controller.ts
        │       └── routes/
        │           ├── chat_routes.ts
        │           ├── customer_routes.ts
        │           ├── message_routes.ts
        │           ├── messageStorage_routes.ts
        │           └── webhook_routes.ts
        ├── application/
        │   └── services/
        │       ├── chat_service.ts
        │       ├── customer_service.ts
        │       ├── message_service.ts
        │       ├── messageStorage_service.ts
        │       └── pythonCommunication.ts
        ├── config/
        │   ├── data_source.ts
        │   └── socket.ts
        ├── cron/
        │   └── inactiveChatCron.ts
        ├── domain/
        │   └── entities/
        │       ├── chat_entity.ts
        │       ├── customer_entity.ts
        │       ├── message_entity.ts
        │       ├── messageStorage_entity.ts
        │       └── summary_entity.ts
        ├── handleUtils/
        │   ├── apiResponse.ts
        │   └── logger.ts
        ├── infrastructure/
        │   └── repositories/
        │       ├── chat_repository.ts
        │       ├── customer_repository.ts
        │       ├── message_repository.ts
        │       ├── messageStorage_repository.ts
        │       └── summary_repository.ts
        ├── main.ts
        ├── middlewares/
        │   └── errorHandleMiddleware.ts
        ├── scripts/
        │   ├── test_client.ts
        │   └── test_summary.ts
        └── sql/
            ├── kai_dataTest.sql
            └── kai_structure.sql
```

---

## 🔐 Variables de Entorno

### `.env` – Python

```ini
# Qdrant
QDRANT_URL="<URL del servidor Qdrant>"
QDRANT_COLLECTION_NAME="asesorias"
QDRANT_API_KEY="<tu_api_key_qdrant>"

# Gemini
GEMINI_API_KEY="<tu_api_key_gemini>"

# Base de datos MySQL
DB_HOST="mysql+pymysql://usuario:contraseña@host:puerto/nombre_db"

# Ejemplo real:
# QDRANT_URL="https://8e87159f-07c4-46fb-9688-c94e61b8becb.us-east4-0.gcp.cloud.qdrant.io"
# QDRANT_COLLECTION_NAME="asesorias"
# GEMINI_API_KEY="AIzaSy..."
# QDRANT_API_KEY="eyJhbGci..."
# DB_HOST="mysql+pymysql://kai_dev:M76y$ever420*25@173.249.28.46:3306/kai_agent_db"
```

### `.env` – Node.js

```ini
DB_HOST="<host>"
DB_USER="<usuario>"
DB_PASSWORD="<contraseña>"
DB_NAME="<nombre_db>"
DB_PORT="3306"

# Ejemplo real:
# DB_HOST="173.249.28.46"
# DB_USER="kai_dev"
# DB_PASSWORD="M76y$ever420*25"
# DB_NAME="kai_agent_db"
# DB_PORT="3306"
```

---

## ⚙️ Comandos de Inicialización

```bash
# Python
python3 -m venv venv                # Crear entorno virtual
source venv/bin/activate            # Activar entorno virtual (Linux/Mac)
venv\Scripts\activate               # Activar entorno virtual (Windows)
pip install -r requirements.txt     # Instalar dependencias
uvicorn app.main:app --reload       # Levantar API FastAPI en modo desarrollo

# Node.js
cd backend
npm install                         # Instalar dependencias
npm run main                        # Iniciar backend principal
npm run test_client                 # Probar conexión vía socket
npm run test_summary                # Probar generación de resumen
```

---

## 🔄 Flujo de Funcionamiento del Bot

1. Solicita nombre y teléfono del usuario.
2. Extrae contexto usando LangGraph.
3. Busca información relevante en Qdrant.
4. Genera respuestas con Gemini.
5. Almacena mensajes y resumen al finalizar.
6. Ofrece soluciones prácticas, capacitación o producto.

---

### 🧩 Flujo LangGraph y Tools Python

El flujo conversacional está orquestado mediante **LangGraph**, donde cada nodo representa una acción o validación sobre el estado del usuario. El grafo principal es el siguiente:

```mermaid
graph TD
    load_state --> extract_info
    extract_info --> save_user
    save_user --> save_message
    save_message --> get_history
    get_history --> retrieve_context
    retrieve_context --> build_prompt
    build_prompt --> check_sent
    check_sent -- solución ya enviada --> end
    check_sent -- continuar --> call_gemini
    call_gemini -- respuesta nueva --> save_bot_message
    call_gemini -- ya enviada --> check_AB
    save_bot_message --> check_AB
    check_AB --> save_state
    save_state --> end
    end --> END
```

#### Descripción de nodos principales:
- **load_state**: Carga el estado actual de la sesión desde la base de datos.
- **extract_info**: Extrae datos clave del input del usuario (nombre, empresa, rol, etc.).
- **save_user**: Guarda o actualiza la información del usuario en la base de datos.
- **save_message**: Guarda el mensaje del usuario y actualiza el historial.
- **get_history**: Recupera los últimos mensajes de la sesión.
- **retrieve_context**: Busca contexto relevante en Qdrant usando el input del usuario.
- **build_prompt**: Construye el prompt para el LLM usando el estado y el historial.
- **check_sent**: Verifica si ya se envió una solución previamente.
- **call_gemini**: Envía el prompt a Gemini y obtiene la respuesta.
- **save_bot_message**: Guarda la respuesta generada por el bot.
- **check_AB**: Evalúa si ya se ofrecieron las opciones A y B (venta/capacitación).
- **save_state**: Guarda el estado actualizado de la sesión.
- **end**: Nodo final del flujo.

#### Tools Python implementadas

| Tool                        | Descripción                                                                                 |
|-----------------------------|--------------------------------------------------------------------------------------------|
| extract_user_info_tool      | Extrae nombre, empresa, rol y teléfono del input del usuario.                               |
| save_user_tool              | Guarda o actualiza la información del usuario en la base de datos.                          |
| retrieve_context_tool       | Busca contexto relevante en Qdrant usando el input del usuario.                             |
| get_history_tool            | Recupera los últimos mensajes de la sesión para el usuario.                                 |
| save_message_tool           | Guarda un mensaje (usuario o bot) y actualiza el historial.                                 |
| build_prompt_tool           | Construye el prompt para el LLM usando el estado y el historial.                            |
| call_gemini_tool            | Envía el prompt a Gemini y obtiene la respuesta.                                            |
| check_already_sent_tool     | Verifica si ya se envió una solución previamente en la conversación.                         |
| check_AB_tool               | Evalúa si ya se ofrecieron las opciones A y B (venta/capacitación).                         |
| save_state_tool             | Guarda o actualiza el estado de la sesión en la base de datos.                              |
| get_state_tool              | Recupera el estado de la sesión desde la base de datos.                                     |
| delete_state_tool           | Elimina el estado de la sesión de la base de datos.                                         |

Cada tool es un bloque reutilizable que permite modularidad y trazabilidad en el flujo conversacional.

---

## 🗃️ Bases de Datos

### 📋 Relacional (MySQL)

- `customer`: Datos del cliente.
- `chat`: Sesiones activas/inactivas.
- `messages`: Historial conversacional.
- `messageStorage`: Logs y respaldo.

### 📦 Vectorial (Qdrant)

- Embeddings semánticos indexados para búsqueda por similitud.
- Uso de `sentence-transformers`.

---

## 📏 Reglas de Comportamiento del Bot

(Resumen de `bot_regulations.py`)

- No iniciar asesoría sin datos básicos del cliente (nombre y teléfono).
- Mantener coherencia y continuidad en la conversación.
- Formular preguntas para obtener contexto específico y relevante.
- Presentar múltiples soluciones adaptadas al caso del cliente.
- Confirmar aceptación del cliente antes de ejecutar cualquier acción.
- No suponer ni dar respuestas genéricas o poco fundamentadas.
- Evitar sugerir herramientas listas sin justificación clara.
- Registrar y almacenar todo el historial conversacional y resúmenes.
- Sugerir siempre una acción final: venta de producto o capacitación personalizada.

---

## 🧪 API - Endpoints

### 🔸 FastAPI (Python)

| Ruta      | Método | Descripción                                 |
|-----------|--------|---------------------------------------------|
| /chat     | POST   | Envía mensaje al bot y obtiene respuesta     |

### 🔹 Express (Node.js)

| Recurso           | Ruta Base           | Acciones Disponibles                        |
|-------------------|---------------------|---------------------------------------------|
| Customers         | /customers          | CRUD y búsqueda por teléfono o ID           |
| Chats             | /chats              | Crear, actualizar, finalizar sesión         |
| Messages          | /messages           | Crear mensaje, obtener historial            |
| MessageStorage    | /messageStorage     | Logs y respaldo de mensajes                 |
| Webhook           | /webhook            | Recepción de eventos externos               |

---

## 🧪 Scripts y Datos de Prueba

- `app/infrastructure/sql/kai_dataTest.sql`: Datos ficticios para pruebas de MySQL.
- `app/infrastructure/sql/setupDB.py`: Script de inicialización y configuración de la base de datos.
- `app/infrastructure/sql/message_saver.py`, `customer_saver.py`, `state_saver.py`: Scripts para persistencia de datos desde Python.
- `backend/src/sql/kai_dataTest.sql`: Datos ficticios para pruebas desde Node.js.
- `backend/src/sql/kai_structure.sql`: Estructura de la base de datos MySQL.
- `backend/src/scripts/test_client.ts`: Prueba de conexión vía socket.
- `backend/src/scripts/test_summary.ts`: Prueba de generación de resumen.
- `text_gemini.py`: Test de integración Gemini.

---

## ✅ Sugerencias del Bot (Post-Solución)

Cuando el cliente acepte una solución, el bot debe sugerir dos caminos:

### ➕ Formato

> Opción 1: Venta del producto
> ****Opción 2:** Capacitación personalizada

### ✨ Ejemplo de Respuesta

> ¡Perfecto! Me alegra que estés de acuerdo con la solución. Para implementarla, puedes elegir una de estas opciones:
>
> 🔹 **Opción 1 – Venta del producto:**
>
> Un asesor comercial se pondrá en contacto contigo para iniciar el proceso de adquisición.
>
> 🔹 **Opción 2 – Capacitación:**
>
> Puedes agendar una sesión en nuestra plataforma. Te enviaremos el enlace para elegir la fecha que más te convenga.

---

## 📌 Conclusión

**KAI** representa una solución escalable para brindar atención automatizada, combinando inteligencia artificial, almacenamiento relacional y búsquedas semánticas. Está diseñado para integrarse fácilmente con WhatsApp, dashboards o sistemas empresariales, ofreciendo asistencia eficiente y adaptable.

---

📅 **Última actualización:** 8 de junio de 2024