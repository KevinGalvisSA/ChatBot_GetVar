# app/infrastructure/factories/extract_info.py

import re
from typing import Dict, Optional

class InfoExtractor:
    def __init__(self):
        # Patrones clave para detectar campos
        self.patterns = {
            'name': [
                r"(?:mi\s+nombre\s+es|me\s+llamo|soy|puedes\s+llamarme|me\s+dicen)\s+([A-Za-zÁÉÍÓÚáéíóúÑñ]+(?:\s+[A-Za-zÁÉÍÓÚáéíóúÑñ]+){0,3})",
            ],
            'phone': [
                r"(?:n[uú]mero\s+de\s+tel[eé]fono\s+es|tel[eé]fono\s*[:\-]?|contactarme\s+al|celular\s*[:\-]?|ll[aá]mame\s+al|mi\s+celular\s+es)?\s*(\+?\d[\d\s\-]{6,15})"
            ],
            'company': [
                r"(?:trabajo\s+en|pertenezco\s+a|en\s+la\s+empresa\s+|trabajo\s+para|vengo\s+de|formo\s+parte\s+de|laboro\s+en|soy\s+parte\s+de)\s*([A-Za-zÁÉÍÓÚáéíóúÑñ0-9&.\- ]{2,40})",
                r"(?:mi\s+empresa\s+es|la\s+compañ[ií]a\s+en\s+la\s+que\s+trabajo\s+es)\s*([A-Za-zÁÉÍÓÚáéíóúÑñ0-9&.\- ]{2,40})",
                r"una\s+empresa\s+de\s+[a-záéíóúñ\s]+",
                r"una\s+compañ[ií]a\s+de\s+[a-záéíóúñ\s]+",
                r"empresa\s+de\s+[a-záéíóúñ\s]+"
            ],
            'rol': [
                r"(?:me\s+desempeñ[oó]?\s+como|mi\s+rol\s+es|trabajo\s+como|soy\s+el|soy\s+la|soy\s+un|soy\s+una|mi\s+puesto\s+es|ocupo\s+el\s+puesto\s+de|mi\s+cargo\s+es|ejerc[oó]\s+como)\s*([A-Za-zÁÉÍÓÚáéíóúÑñ ]{2,40})",
                r"^(administrador|gerente|director|encargado|coordinador|analista|desarrollador|ingeniero|técnico|consultor|vendedor|secretaria|auxiliar|presidente|ceo|cto|cfo|cofundador|fundador|representante)$"
            ]
        }

        self.rol_company_pattern = r"soy\s+(?:el|la|un|una)?\s*(?P<rol>[a-záéíóúñ ]{2,40}?)\s+(?:de|en|para)\s+(?:una|un|el|la)?\s*(?P<empresa>[a-záéíóúñ0-9&.\- ]{2,40})"

        self.common_roles = {
            "administrador", "gerente", "director", "encargado", "coordinador",
            "analista", "desarrollador", "ingeniero", "técnico", "consultor",
            "vendedor", "secretaria", "auxiliar", "presidente", "ceo", "cto",
            "cfo", "cofundador", "fundador", "representante"
        }

        self.stopwords = {
            "hola", "buenos", "días", "buenas", "tardes", "noches",
            "gracias", "ok", "vale", "listo", "me", "parece", "bien", "sí", "no"
        }

    def clean_rol(self, text: str) -> str:
        text = re.sub(r"\b(el|la|un|una|de)\b", "", text, flags=re.IGNORECASE)
        palabras = text.strip().split()
        return " ".join(palabras).title() if palabras else text.title()

    def clean_company(self, text: str) -> Optional[str]:
        if not text:
            return None
        # Quitar frases genéricas
        generic_phrases = [
            r"una\s+empresa\s+de\s+[a-záéíóúñ\s]+",
            r"una\s+compañ[ií]a\s+de\s+[a-záéíóúñ\s]+",
            r"empresa\s+de\s+[a-záéíóúñ\s]+"
        ]
        for phrase in generic_phrases:
            text = re.sub(phrase, "", text, flags=re.IGNORECASE)
        return text.strip().title() if text.strip() else None

    def looks_like_name(self, candidate: str) -> bool:
        words = candidate.split()
        if len(words) > 3:
            return False
        # Si tiene mayúsculas iniciales (ideal)
        if all(w[0].isupper() for w in words):
            return True
        # Si no, pero no tiene números, signos ni stopwords, lo aceptamos como posible nombre
        words_lower = [w.lower() for w in words]
        if any(w in self.stopwords for w in words_lower):
            return False
        if any(not w.isalpha() for w in words):
            return False
        return True

    def extract(self, text: str) -> Dict[str, Optional[str]]:
        extracted_info = {'name': None, 'phone': None, 'company': None, 'rol': None}

        # Primero intentar patrón "soy <rol> de <empresa>"
        match = re.search(self.rol_company_pattern, text, re.IGNORECASE)
        if match:
            raw_rol = match.group("rol").strip()
            raw_company = match.group("empresa").strip()
            extracted_info['rol'] = self.clean_rol(raw_rol)
            extracted_info['company'] = self.clean_company(raw_company)

        # Buscar en cada categoría con sus patrones
        for key, patterns in self.patterns.items():
            if extracted_info[key] is not None:
                continue
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    value = match.group(1).strip()
                    if key == 'phone':
                        value = re.sub(r"[^\d+]", "", value)
                        extracted_info[key] = value
                    elif key == 'rol':
                        extracted_info[key] = self.clean_rol(value)
                    elif key == 'company':
                        extracted_info[key] = self.clean_company(value)
                    else:
                        extracted_info[key] = value.title()
                    break  # deja de buscar patrones si ya encontró uno

        # Si no detectó nombre ni rol, intentar detectar texto suelto corto (1 a 3 palabras)
        words = text.strip().split()
        if not extracted_info['name'] and not extracted_info['rol'] and 1 <= len(words) <= 3:
            candidate = " ".join(words).strip()
            if self.looks_like_name(candidate) and candidate.lower() not in self.common_roles:
                extracted_info['name'] = candidate.title()
            else:
                # Para roles sueltos sin contexto, lo asignamos en minúscula
                extracted_info['rol'] = candidate.lower()

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
