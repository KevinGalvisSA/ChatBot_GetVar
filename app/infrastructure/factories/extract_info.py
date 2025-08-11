import re
from typing import Dict, Optional

class InfoExtractor:
    def __init__(self):
        # Frases que indican que el usuario no está dando datos reales
        self.invalid_responses = set(map(str.lower, [
            "hola", "ok", "vale", "si", "sí", "no", "me parece bien", "está bien", "correcto", "claro", 
            "perfecto", "genial", "entendido", "listo", "de acuerdo",
            "gracias", "gracias por la información", "gracias por tu ayuda", 
            "gracias por tu respuesta", "gracias por tu tiempo",
            "no tengo más preguntas", "no tengo dudas", "no necesito más información",
            "no necesito ayuda", "no necesito nada más", "me das mas información",
            "no tengo nada más que decir", "no tengo nada más que preguntar",
            "no tengo nada más que añadir", "no tengo nada más que comentar",
            "no tengo nada más que aportar", "no tengo nada más que ofrecer",
            "no tengo nada más que sugerir"
        ]))

        # Patrones para extracción con ignorancia de mayúsculas/minúsculas
        self.patterns = {
            'name': [
                r"(?:\bmi\s+nombre\s+es\b|\bme\s+llamo\b)\s+(?!hola|buenos|buenas|saludos)([a-záéíóúñ]{2,20}(?:\s+[a-záéíóúñ]{2,20}){0,2})",
                r"\b(?:nombre\s*[:\-]?)\s*(?!hola|buenos|buenas)([a-záéíóúñ]{2,20}(?:\s+[a-záéíóúñ]{2,20}){0,2})"
            ],
            'phone': [
                r"(?:\+?\d[\d\s\-\(\)]{6,20})"
            ],
            'company': [
                r"(?:trabajo\s+en|pertenezco\s+a|en\s+la\s+empresa\s+|trabajo\s+para|vengo\s+de)\s*([a-záéíóúñ0-9&.\- ]{2,})"
            ],
            'rol': [
                r"(?:me\s+desempeñ[oó]?\s+como|mi\s+rol\s+es|trabajo\s+como|soy\s+(?![a-záéíóúñ]+\b))\s*([a-záéíóúñ ]{2,30})",
                r"^(administrador|gerente|director|encargado|coordinador|analista|desarrollador|ingeniero|técnico|consultor|vendedor|secretaria|auxiliar|ceo|presidente)$"
            ]
        }

        # Patrones combinados (rol + empresa)
        self.rol_company_patterns = [
            r"soy\s+(?:el|la|un|una)?\s*(?P<rol>[a-záéíóúñ ]{2,30}?)\s+de\s+(?:una|un|el|la)?\s*(?P<empresa>[a-záéíóúñ0-9&.\- ]{2,})",
            r"trabajo\s+en\s+(?P<empresa>[a-záéíóúñ0-9&.\- ]{2,})\s+y\s+soy\s+(?:el|la|un|una)?\s*(?P<rol>[a-záéíóúñ ]{2,30})"
        ]

    def clean_rol(self, text: str) -> str:
        return " ".join(text.strip().split()).title()

    def clean_company(self, text: str) -> Optional[str]:
        if not text:
            return None
        generic_phrases = [
            r"una\s+empresa\s+de\s+[a-záéíóúñ\s]+",
            r"una\s+compañ[ií]a\s+de\s+[a-záéíóúñ\s]+",
            r"empresa\s+de\s+[a-záéíóúñ\s]+"
        ]
        for phrase in generic_phrases:
            text = re.sub(phrase, "", text, flags=re.IGNORECASE)
        return text.strip().title() if text.strip() else None

    def extract(self, text: str) -> Dict[str, Optional[str]]:
        text_stripped = text.strip()
        text_clean = text_stripped.lower()

        # Filtro de respuestas inválidas
        if text_clean in self.invalid_responses:
            return {k: None for k in ["name", "phone", "company", "rol"]}

        extracted_info = {k: None for k in ["name", "phone", "company", "rol"]}

        # Detectar patrón combinado rol + empresa
        for pattern in self.rol_company_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                raw_rol = match.group("rol").strip()
                raw_company = match.group("empresa").strip()
                extracted_info["rol"] = self.clean_rol(raw_rol)
                extracted_info["company"] = self.clean_company(raw_company)
                break

        # Detectar cada dato individualmente
        for key, patterns in self.patterns.items():
            if extracted_info[key]:
                continue
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    value = match.group(1).strip()
                    if key == "phone":
                        value = re.sub(r"[^\d+]", "", value)
                    elif key == "rol":
                        value = self.clean_rol(value)
                    elif key == "company":
                        value = self.clean_company(value)
                    elif key == "name":
                        # Evitar falsos positivos tipo "Hola"
                        if len(value.split()) == 1 and value.lower() in ["hola", "buenos", "buenas", "saludos"]:
                            continue
                        if re.fullmatch(self.patterns['rol'][1], value, re.IGNORECASE):
                            continue
                        value = value.title()
                    extracted_info[key] = value
                    break

        # Evitar que rol y nombre sean iguales
        if extracted_info["name"] and extracted_info["rol"]:
            if extracted_info["name"].lower() == extracted_info["rol"].lower():
                if len(extracted_info["name"].split()) == 1:
                    extracted_info["name"] = None
                elif len(extracted_info["rol"].split()) == 1:
                    extracted_info["rol"] = None

        return extracted_info

    def validate_extracted_info(self, extracted_info: Dict[str, Optional[str]]) -> str:
        missing = []
        if not extracted_info['name']:
            missing.append("tu nombre")
        if not extracted_info['phone']:
            missing.append("tu número de teléfono")

        if missing:
            return f"Para continuar necesito {', y '.join(missing)}. ¿Podrías proporcionármelos por favor? 📝"
        return "✅ ¡Gracias por la información! Ahora dime, ¿en qué puedo ayudarte?"
