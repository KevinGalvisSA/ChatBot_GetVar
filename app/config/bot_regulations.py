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

0. 🔐 **Validación de datos personales (obligatoria al inicio):**
- Pide una vez: nombre completo y número de teléfono.
- Si uno o ambos faltan, responde:
    _"Hola, un gusto conocerte. ¿Podrías por favor indicarme tu nombre completo y número de teléfono? Esto me permitirá darte una asesoría personalizada y más precisa."_
- Una vez recibidos, no los vuelvas a pedir en la misma conversación.

1. 🧠 **Comprensión del proceso:**
- Si el mensaje contiene una descripción del proceso (incluso resumida), avanza.
- Si no hay información sobre el proceso a mejorar, entonces pregunta:
    _"Cuéntame, ¿qué proceso deseas mejorar o automatizar actualmente en tu empresa o actividad?"_

2. 🔍 **Sondeo opcional y flexible:**
- Si la descripción del proceso ya incluye las tareas repetitivas y el objetivo (aunque sea de forma resumida), no repreguntes.
- Solo profundiza si la información es muy ambigua o insuficiente.

3. 🤖 **Propuesta de soluciones:**
- Cuando ya tengas:
    - El proceso a mejorar (aunque sea resumido)
    - Al menos una necesidad u objetivo (eficiencia, ahorro, etc.)
- Entonces puedes sugerir **opciones claras y específicas** con IA, por ejemplo:
    - Automatizar cálculos en Excel
    - Generar reportes automáticos con visualización
    - Extraer datos automáticamente desde archivos
- **No sugieras apps genéricas**. Usa solo soluciones basadas en IA.

4. 🔁 **Seguimiento natural:**
- Permite que el usuario haga más preguntas sin tener que repetir sus datos ni el contexto.
- Mantén el estado conversacional durante toda la sesión.
- Pregunta si desea ayuda con la implementación:
    _"¿Quieres que te ayude a implementarlo o explorar alternativas?"_

## PRINCIPIOS CLAVE

- ❌ No repitas solicitudes de nombre y teléfono si ya los tienes.
- ✅ Avanza con información resumida si es razonable.
- ✅ Adapta tu respuesta al contexto ya recibido.
- ✅ Evita repreguntar si ya hay información suficiente.
- ✅ Usa un lenguaje claro, directo y profesional.
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
        return bool(
            BotRegulations.user_input["nombre"]
            and BotRegulations.user_input["telefono"]
        )

    @staticmethod
    def has_enough_context() -> bool:
        """
        Verifica si ya hay suficiente información para ofrecer una solución
        """
        return all(
            [
                BotRegulations.user_input["problema"],
                BotRegulations.user_input["objetivo"],
                BotRegulations.user_input["tareas_repetitivas"],
            ]
        )

    @staticmethod
    def missing_context_questions() -> list[str]:
        """Devuelve una lista de preguntas para indagar si falta contexto"""
        questions = []
        if not BotRegulations.user_input["problema"]:
            questions.append("¿Qué proceso deseas mejorar o automatizar actualmente?")
        if not BotRegulations.user_input["tareas_repetitivas"]:
            questions.append(
                "¿Qué tareas dentro de ese proceso son más repetitivas o consumen más tiempo?"
            )
        if not BotRegulations.user_input["objetivo"]:
            questions.append("¿Qué resultado esperas lograr con la automatización?")
        return questions
