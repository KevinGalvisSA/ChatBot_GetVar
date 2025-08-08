import re
from typing import Dict, Optional

class InfoExtractor:
    def __init__(self):
        self.patterns = {
            'name': [
                r"(?:mi\s+nombre\s+es|me\s+llamo|soy)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){0,2})",
                r"\b(?:nombre\s*[:\-]?)\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){0,2})",
                r"^soy\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){0,2})$"
            ],
            'phone': [
                r"(?:n[uú]mero\s+de\s+tel[eé]fono\s+es|tel[eé]fono\s*[:\-]?|contactarme\s+al|celular\s*[:\-]?|ll[aá]mame\s+al)?\s*(\+?\d[\d\s\-]{6,15})"
            ],
            'company': [
                r"(?:trabajo\s+en|pertenezco\s+a|en\s+la\s+empresa\s+|trabajo\s+para|vengo\s+de)\s*([A-Za-zÁÉÍÓÚáéíóúÑñ0-9&.\- ]{2,})",
                r"(?:trabajo\s+)([A-Za-zÁÉÍÓÚáéíóúÑñ0-9&.\- ]{2,})",
                r"(?:vengo\s+de)\s*([A-Za-zÁÉÍÓÚáéíóúÑñ0-9&.\- ]{2,})",
                r"una\s+empresa\s+de\s+[a-záéíóúñ\s]+",
                r"una\s+compañ[ií]a\s+de\s+[a-záéíóúñ\s]+",
                r"empresa\s+de\s+[a-záéíóúñ\s]+"
            ],
            'rol': [
                r"(?:me\s+desempeñ[oó]?\s+como|mi\s+rol\s+es|trabajo\s+como|soy\s+el|soy\s+la|soy\s+un|soy\s+una)\s*([A-Za-zÁÉÍÓÚáéíóúÑñ ]{2,30})",
                r"^(administrador|gerente|director|encargado|coordinador|analista|desarrollador|ingeniero|técnico|consultor|vendedor|secretaria|auxiliar|ceo|presidente)$"
            ]
        }

        # Múltiples patrones rol + empresa
        self.rol_company_patterns = [
            r"soy\s+(?:el|la|un|una)?\s*(?P<rol>[a-záéíóúñ ]{2,30}?)\s+de\s+(?:una|un|el|la)?\s*(?P<empresa>[a-záéíóúñ0-9&.\- ]{2,})",
            r"trabajo\s+en\s+(?P<empresa>[a-záéíóúñ0-9&.\- ]{2,})\s+y\s+soy\s+(?:el|la|un|una)?\s*(?P<rol>[a-záéíóúñ ]{2,30})",
            r"trabajo\s+(?P<empresa>[a-záéíóúñ0-9&.\- ]{2,})\s+y\s+soy\s+(?:el|la|un|una)?\s*(?P<rol>[a-záéíóúñ ]{2,30})"
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
        extracted_info = {
            'name': None,
            'phone': None,
            'company': None,
            'rol': None
        }

        # Intentar patrón combinado
        for pattern in self.rol_company_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                raw_rol = match.group("rol").strip()
                raw_company = match.group("empresa").strip()
                if raw_rol and raw_company:
                    extracted_info['rol'] = self.clean_rol(raw_rol)
                    extracted_info['company'] = self.clean_company(raw_company)
                    break

        # Extraer uno por uno
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
                    break

        # Evitar rol y nombre duplicados
        if (
            extracted_info["name"] 
            and extracted_info["rol"] 
            and extracted_info["name"].lower() == extracted_info["rol"].lower()
        ):
            # Si ambos son iguales y de una sola palabra, mejor eliminar uno
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
