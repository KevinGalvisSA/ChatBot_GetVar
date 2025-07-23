import re
from typing import Dict, Optional

class InfoExtractor:
    def __init__(self):
        """
        Inicializa el extractor de información con patrones ampliados para nombre y teléfono.
        """
        self.patterns = {
            'name': r"(?:mi\s+nombre\s+es|nombre\s*[:\-]?|me\s+llamo|soy)\s+([A-Za-zÁÉÍÓÚáéíóúÑñ]+(?:\s+[A-Za-zÁÉÍÓÚáéíóúÑñ]+){0,2})",
            'phone_number': r"(?:n[uú]mero\s+de\s+tel[eé]fono\s+es|tel[eé]fono\s*[:\-]?|contactarme\s+al|celular\s*[:\-]?|ll[aá]mame\s+al)?\s*(\+?\d[\d\s\-]{6,15})"
        }

    def extract(self, text: str) -> Dict[str, Optional[str]]:
        """
        Extrae nombre y teléfono del texto del usuario.
        
        Args:
        - text (str): Entrada del usuario.
        
        Returns:
        - dict: Con las claves 'name' y 'phone_number', si fueron encontrados.
        """
        extracted_info: Dict[str, Optional[str]] = {
            'name': None,
            'phone_number': None
        }

        # Buscar nombre
        name_match = re.search(self.patterns['name'], text, re.IGNORECASE)
        if name_match:
            extracted_info['name'] = name_match.group(1).strip()

        # Buscar teléfono
        phone_number_match = re.search(self.patterns['phone_number'], text, re.IGNORECASE)
        if phone_number_match:
            extracted_info['phone_number'] = re.sub(r"[^\d+]", "", phone_number_match.group(1).strip())

        return extracted_info

    def validate_extracted_info(self, extracted_info: Dict[str, Optional[str]]) -> str:
        """
        Devuelve un mensaje en función de los campos faltantes.

        Args:
        - extracted_info (dict): Info extraída del mensaje.
        
        Returns:
        - str: Mensaje indicando qué falta o si todo está listo.
        """
        missing = []
        if not extracted_info['name']:
            missing.append("tu nombre")
        if not extracted_info['phone_number']:
            missing.append("tu número de teléfono")

        if missing:
            return f"Para continuar necesito {', y '.join(missing)}. ¿Podrías proporcionármelos por favor?"

        return "✅ ¡Gracias por la información! Ahora dime, ¿en qué puedo ayudarte?"
    
