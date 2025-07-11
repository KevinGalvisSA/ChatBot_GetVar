import os
from dotenv import load_dotenv  # Asegúrate de cargar las variables del archivo .env
from app.models.context_chunk import ContextChunk  # type: ignore # Asegúrate de que esta clase esté definida correctamente en tu proyecto
from app.config.bot_regulations import BotRegulations  # Asegúrate de que este archivo esté correctamente configurado
import google.generativeai as genai  # type: ignore

# Cargar las variables del archivo .env
load_dotenv()

# Asegúrate de que la clave de API esté correctamente cargada
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise Exception("La clave de API de Gemini no está configurada.")

# Configura la API de Gemini
genai.configure(api_key=GEMINI_API_KEY)  # type: ignore

# Definimos una clase mock de ContextChunk para probar
class ContextChunk:
    def __init__(self, text: str):
        self.text = text

# Implementamos la función que quieres probar
def answer_with_gemini(question: str, chunks: list) -> str:
    try:
        # Verificar si la clave de API está configurada correctamente
        if not GEMINI_API_KEY:
            raise Exception("La clave de API de Gemini no está configurada.")

        # Configurar el modelo de Gemini
        model = genai.GenerativeModel("models/gemini-1.5-pro")  # type: ignore

        # Crear el contexto a partir de los fragmentos
        context = "\n".join([chunk.text for chunk in chunks])

        # Obtener el reglamento del bot
        bot_intro = BotRegulations.get_rule("intro")  # Si no tienes este archivo, omítelo o crea una función mock

        # Crear el prompt para enviar a Gemini usando f-string para interpolar las variables
        prompt = f"""
        {bot_intro}

        ### CONTEXTO:
        {context}

        ### PREGUNTA:
        {question}

        ### RESPONDE CON ENFOQUE EN LA SOLUCIÓN:
        Mantén la respuesta centrada en proporcionar soluciones claras y prácticas que ayuden al cliente a automatizar o mejorar su proceso, sin desviarte a temas irrelevantes. Usa un lenguaje sencillo y directo. 
        """

        # Llamar a la API de Gemini para generar la respuesta
        response = model.generate_content(prompt)

        # Si la respuesta no tiene texto, lanzamos un error
        if not response or not response.text:
            raise Exception("Gemini no respondió correctamente.")

        return response.text
    
    except Exception as e:
        return f"❌ Error al usar Gemini: {str(e)}"

# Prueba con una pregunta simple
question = "Hola! Mi nombre es Kevin Galvis y mi numero telefonico es 3056472933. Puedo saber como automatizar un bot que haga deteccion de fraudes?"
chunks = [ContextChunk("Soy un chatbot diseñado para ayudarte.")]  # Puedes agregar más fragmentos si lo deseas

# Llamar a la función y ver la respuesta
response = answer_with_gemini(question, chunks)
print("Respuesta de Gemini:", response)
