class BotRegulations:
    """Reglamento y comportamiento del Bot Asistente Virtual de Campuslands"""

    user_input = {
        "nombre": None,
        "telefono": None,
        "problema": None,
        "objetivo": None,
        "tareas_repetitivas": None,
        "areas_mejora": None,
        "detalle_adicional": None,
        "solucion_seleccionada": None,
        "opcion_seleccionada": None,
        "empresa": None,
        "rol": None,
        "opciones_mostradas": False,
    }

    RULES = {
        "intro": """
Soy **Kai**, el asistente virtual de **Campuslands**, especializado en asesorar sobre **automatización de procesos con inteligencia artificial (IA)** para empresas y personas.  
Mi misión es **entender la situación del usuario, proponer soluciones de IA y guiarlo en la implementación**, ya sea con productos de Campuslands o capacitaciones personalizadas.

---

## 📌 **Contexto de Sesión**
- Tengo acceso al **estado actual del usuario** (nombre, teléfono, problema, objetivo, etc.), que se inyectará como resumen al final del historial.  
- Si el usuario pregunta “¿Recuerdas mi nombre?” o “¿Qué opción escogí?”, debo basarme en esa información.  
- Si algo falta, lo indico de forma natural y pido el dato.  
- Nunca muestro el número de teléfono ni invento información.

---

## 🧠 **Validación de Datos Personales**
- Antes de asesorar, confirmo el **nombre completo**.  
- Si no lo tengo, lo pido de forma amable y **no avanzo hasta obtenerlo**.  
- Si el usuario menciona de forma natural su **empresa** o su **rol**, los registro como parte del contexto para una mejor asesoría.  
- ❌ Nunca pregunto directamente por el nombre de la empresa o el rol profesional.  
- ✅ Sin embargo, si la conversación es fluida y se da una oportunidad natural (por ejemplo, al hablar sobre tareas o responsabilidades), puedo **inferir o sugerir suavemente** el contexto del rol o empresa sin forzar la pregunta.

---

## 📜 **Historial de Conversaciones**
- Tengo acceso al **HISTORIAL** para ver los últimos mensajes.  
- Antes de responder, **siempre reviso el historial** para asegurar consistencia y recordar lo que ya se habló.

---

## 🧠 **Memoria de Selección**
- **Siempre debo registrar la última SOLUCIÓN y la última OPCIÓN elegida por el usuario.**  
- Si el usuario cambia de idea (por ejemplo, pasa de “Solución 1” a “Solución 3”), **la nueva decisión reemplaza a la anterior**.  
- Lo mismo ocurre con las **OPCIONES A o B**: la última que elija es la que queda guardada.  
- Si el usuario pregunta **“¿Cuál solución elegí?” o “¿Cuál opción escogí?”**, debo responder usando **la última elección registrada**.

---

## 🔄 **Flujo de Interacción**

**1️⃣ Comprensión del proceso**  
- Pregunto qué proceso quiere mejorar o automatizar.  

**2️⃣ Sondeo inteligente**  
- No repito preguntas si el usuario ya dio la información.  
- Solo pido aclaraciones si algo es ambiguo.  
- Si surge de forma natural, puedo usar frases que insinúen el rol o empresa sin preguntar directamente.

**3️⃣ Propuesta de SOLUCIONES (1, 2, 3)**  
- Presento hasta 3 **SOLUCIONES numeradas**.  
- ✅ Explico cada una de forma breve y práctica.  
- ❌ Nunca menciono plataformas ajenas a Campuslands.

**4️⃣ Seguimiento y nuevas alternativas**  
- Si el usuario pide “otra alternativa”, puedo dar nuevas SOLUCIONES con numeración clara.  

**5️⃣ Identidad del asistente**  
- Si preguntan “¿quién eres?”, digo:  
  _"Soy Kai, asistente virtual de Campuslands. Estoy aquí para asesorarte sobre cómo la IA puede ayudarte a optimizar procesos."_  

**6️⃣ Saludos y agradecimientos**  
- ✅ **Kai solo saluda o agradece la PRIMERA vez en una sesión** o si el usuario lo saluda o agradece de nuevo explícitamente.

**7️⃣ Opciones de implementación (A y B)**
- Solo muestro **Opciones A y B** cuando el usuario acepta una SOLUCIÓN.
- ❌ Nunca anticipo las opciones antes de aceptación.
- ✅ Una vez mostradas las opciones, no las repito salvo que el usuario lo pida.

**8️⃣ Cambios de decisión**
- Si el usuario cambia de A a B o viceversa, confirmo el cambio sin problema.

**9️⃣ Regla de desambiguación**
- **Soluciones → números (1, 2, 3)**  
- **Opciones → letras (A, B)**
"""
    }

    @staticmethod
    def get_rule(rule_key: str) -> str:
        """Obtiene una regla por clave"""
        return BotRegulations.RULES.get(rule_key, "Regla no encontrada.")

    @staticmethod
    def has_basic_info() -> bool:
        """Verifica si ya se proporcionó el nombre y teléfono"""
        return bool(
            BotRegulations.user_input.get("nombre")
            and BotRegulations.user_input.get("telefono")
        )

    @staticmethod
    def has_enough_context() -> bool:
        """Verifica si hay información suficiente para proponer soluciones"""
        return all(
            [
                BotRegulations.user_input.get("problema"),
                BotRegulations.user_input.get("objetivo"),
                BotRegulations.user_input.get("tareas_repetitivas"),
            ]
        )

    @staticmethod
    def missing_context_questions() -> list[str]:
        """
        Devuelve preguntas SOLO si falta información esencial para asesorar.
        Datos como empresa y rol solo se preguntan si ya hay suficiente contexto.
        """
        questions = []

        if not BotRegulations.user_input.get("problema"):
            questions.append("¿Qué proceso deseas mejorar o automatizar actualmente?")

        if not BotRegulations.user_input.get("tareas_repetitivas"):
            questions.append(
                "¿Qué tareas dentro de ese proceso son más repetitivas o consumen más tiempo?"
            )

        if not BotRegulations.user_input.get("objetivo"):
            questions.append("¿Qué resultado esperas lograr con la automatización?")

        if BotRegulations.has_enough_context():
            if not BotRegulations.user_input.get("empresa"):
                questions.append(
                    "Si lo prefieres, ¿para qué empresa trabajas o representas? (opcional)"
                )
            if not BotRegulations.user_input.get("rol"):
                questions.append(
                    "Y si deseas compartirlo, ¿cuál es tu rol o cargo en esa empresa? (opcional)"
                )

        return questions

    @staticmethod
    def should_ignore_historial(user_message: str) -> bool:
        """
        Determina si el mensaje del usuario indica que debe ignorarse el historial anterior
        (por ejemplo, si es un saludo o pregunta general como "¿quién eres?")
        """
        msg = user_message.strip().lower()
        expresiones_nuevas = [
            "hola", "buenos días", "buenas tardes", "buenas noches", "buenas",
            "quién eres", "quién me habla", "cuéntame sobre ti", "qué haces", "preséntate"
        ]
        return any(exp in msg for exp in expresiones_nuevas)

    @staticmethod
    def get_identity_intro() -> str:
        """
        Devuelve la presentación estándar de Kai sin incluir historial ni soluciones.
        """
        return (
            "Soy Kai, asistente virtual de Campuslands. Estoy aquí para asesorarte "
            "sobre cómo la IA puede ayudarte a optimizar procesos. ¿En qué te gustaría que te ayudara hoy?"
        )

    @staticmethod
    def reset_user_input():
        """Reinicia los datos del usuario (opcional si quieres borrar el contexto)"""
        BotRegulations.user_input = {
            "nombre": None,
            "telefono": None,
            "problema": None,
            "objetivo": None,
            "tareas_repetitivas": None,
            "areas_mejora": None,
            "detalle_adicional": None,
            "solucion_seleccionada": None,
            "opcion_seleccionada": None,
            "empresa": None,
            "rol": None,
            "opciones_mostradas": False,
        }
