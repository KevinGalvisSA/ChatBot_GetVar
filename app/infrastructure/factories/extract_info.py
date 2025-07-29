import re
from typing import Dict, Optional

class InfoExtractor:
    def __init__(self):
        self.patterns = {
            'name': r"(?:mi\s+nombre\s+es|nombre\s*[:\-]?|me\s+llamo)\s+([A-Za-zÁÉÍÓÚáéíóúÑñ]+(?:\s+[A-Za-zÁÉÍÓÚáéíóúÑñ]+){0,2})",
            'phone': r"(?:n[uú]mero\s+de\s+tel[eé]fono\s+es|tel[eé]fono\s*[:\-]?|contactarme\s+al|celular\s*[:\-]?|ll[aá]mame\s+al)?\s*(\+?\d[\d\s\-]{6,15})",
            'company': r"(?:trabajo\s+en|pertenezco\s+a|en\s+la\s+empresa\s+)\s*([A-Za-zÁÉÍÓÚáéíóúÑñ0-9&.\- ]{2,})",
            'rol': r"(?:me\s+desempeñ[oó]?\s+como|mi\s+rol\s+es|trabajo\s+como)\s*([A-Za-zÁÉÍÓÚáéíóúÑñ ]{2,})"
        }

        # Patrón mejorado para evitar empresas genéricas como "una empresa de videojuegos"
        self.rol_company_pattern = r"soy\s+(?:el|la|un|una)?\s*(?P<rol>[a-záéíóúñ ]{2,30}?)\s+de\s+(?!una\s+empresa\s+de)(?P<empresa>[a-záéíóúñ0-9&.\- ]{2,})"

        # Frases genéricas que indican empresa sin nombre específico
        self.generic_company_phrases = [
            r"una\s+empresa\s+de\s+[a-záéíóúñ\s]+",
            r"una\s+compañ[ií]a\s+de\s+[a-záéíóúñ\s]+",
            r"empresa\s+de\s+[a-záéíóúñ\s]+"
        ]

    def clean_rol(self, text: str) -> str:
        text = re.sub(r"\b(el|la|un|una|de)\b", "", text, flags=re.IGNORECASE)
        palabras = text.strip().split()
        return palabras[0].title() if palabras else text.title()

    def clean_company(self, text: str) -> Optional[str]:
        for phrase in self.generic_company_phrases:
            text = re.sub(phrase, "", text, flags=re.IGNORECASE)
        text = text.strip().title()
        return text if text else None

    def extract(self, text: str) -> Dict[str, Optional[str]]:
        extracted_info: Dict[str, Optional[str]] = {
            'name': None,
            'phone': None,
            'company': None,
            'rol': None
        }

        # Buscar primero por la estructura especial: "Soy <rol> de <empresa>"
        match = re.search(self.rol_company_pattern, text, re.IGNORECASE)
        if match:
            raw_rol = match.group("rol").strip()
            raw_company = match.group("empresa").strip()

            clean_company = self.clean_company(raw_company)

            if clean_company:
                extracted_info['rol'] = self.clean_rol(raw_rol)
                extracted_info['company'] = clean_company
            else:
                # Solo guardar rol si la empresa no fue válida
                extracted_info['rol'] = self.clean_rol(raw_rol)

        # Buscar otros campos si aún no se han detectado
        for key, pattern in self.patterns.items():
            if extracted_info[key] is not None:
                continue

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

        return extracted_info

    def validate_extracted_info(self, extracted_info: Dict[str, Optional[str]]) -> str:
        missing = []
        if not extracted_info['name']:
            missing.append("tu nombre")
        if not extracted_info['phone']:
            missing.append("tu número de teléfono")

        if missing:
            return f"Para continuar necesito {', y '.join(missing)}. ¿Podrías proporcionármelos por favor?"

        return "✅ ¡Gracias por la información! Ahora dime, ¿en qué puedo ayudarte?"
