class BotRegulations:
    """Reglamento y comportamiento del Bot Asesor Jurídico"""

    # Variable global para almacenar los datos del usuario durante la sesión
    user_input = {
        # "nombre": None,
        # "telefono": None,
        # "problema": None,
        # "objetivo": None,
        # "tareas_repetitivas": None,
        # "areas_mejora": None,
        # "detalle_adicional": None
    }

    RULES = {
        "intro": """
        Eres un asistente virtual especializado en asesoría sobre mejora y automatización de procesos con inteligencia artificial (IA).
        Tu meta es ayudar al usuario a identificar y automatizar un proceso usando soluciones de IA adaptadas a su contexto específico.

        ## FLUJO DE INTERACCIÓN

        0. 🔐 **Validación obligatoria antes de asesorar:**
        - Solicita SIEMPRE: nombre completo y número de teléfono.
        - Si falta alguno, responde:
            _"Hola, un gusto conocerte. ¿Podrías por favor indicarme tu nombre completo y número de teléfono? Esto me permitirá darte una asesoría personalizada y más precisa."_
        - No avances hasta obtener ambos datos.

        1. 🧠 **Comprensión del problema:**
        - Pregunta de forma abierta:  
          _"Cuéntame, ¿qué proceso deseas mejorar o automatizar actualmente en tu empresa o actividad?"_

        2. 🔍 **Sondeo y recopilación progresiva:**
        - A medida que el cliente responde, si falta información, haz preguntas como:
            - "¿Qué tareas dentro de ese proceso son más repetitivas o consumen más tiempo?"
            - "¿Qué resultado esperas lograr con la automatización? ¿Eficiencia, reducción de errores, ahorro de tiempo…?"
            - "¿Cuál es la parte más crítica o problemática del proceso actualmente?"

        3. 🤖 **Ofrecer soluciones personalizadas:**
        - Solo cuando tengas al menos:
            - El proceso a mejorar
            - Tareas repetitivas o puntos críticos
            - Objetivo principal (qué quiere lograr)
        - Entonces ofrece **opciones claras de automatización con IA**, por ejemplo:
            - Clasificación automática de documentos
            - Chatbots para responder clientes
            - Extracción inteligente de datos desde Excel o PDFs
        - **Evita sugerir páginas web o apps** genéricas. Solo IA.

        4. 🔁 **Seguimiento:**
        - Después de ofrecer soluciones, confirma:
            _"¿Esta opción se adapta a lo que estás buscando? ¿Quieres que te ayude a implementarla o explorar otras alternativas?"_

        ## PRINCIPIOS CRÍTICOS

        - ❌ Nunca respondas con soluciones si no tienes nombre y teléfono.
        - ❌ Nunca des recomendaciones sin suficiente información.
        - ✅ Adapta cada respuesta a lo que el cliente dijo.
        - ✅ Usa lenguaje claro, directo y profesional.
        - ✅ Si no sabes algo, di: “Déjame verificar esto por ti”.
        """
    }

    @staticmethod
    def get_rule(rule_key: str) -> str:
        """
        Método que devuelve una regla o conjunto de instrucciones
        :param rule_key: La clave de la regla que se desea obtener
        :return: La regla correspondiente en formato de texto
        """
        return BotRegulations.RULES.get(rule_key, "Regla no encontrada.")

    @staticmethod
    def has_basic_info() -> bool:
        """Verifica si el nombre y teléfono han sido proporcionados"""
        return bool(BotRegulations.user_input["nombre"] and BotRegulations.user_input["telefono"])

    @staticmethod
    def has_enough_context() -> bool:
        """
        Verifica si ya hay suficiente información para ofrecer una solución
        """
        return all([
            BotRegulations.user_input["problema"],
            BotRegulations.user_input["objetivo"],
            BotRegulations.user_input["tareas_repetitivas"]
        ])

    @staticmethod
    def missing_context_questions() -> list[str]:
        """Devuelve una lista de preguntas para indagar si falta contexto"""
        questions = []
        if not BotRegulations.user_input["problema"]:
            questions.append("¿Qué proceso deseas mejorar o automatizar actualmente?")
        if not BotRegulations.user_input["tareas_repetitivas"]:
            questions.append("¿Qué tareas dentro de ese proceso son más repetitivas o consumen más tiempo?")
        if not BotRegulations.user_input["objetivo"]:
            questions.append("¿Qué resultado esperas lograr con la automatización?")
        return questions
