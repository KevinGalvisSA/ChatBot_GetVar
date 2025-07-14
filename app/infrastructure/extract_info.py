import re
from typing import Dict, Optional

class InfoExtractor:
    def __init__(self):
        """
        Inicializa el extractor de información con patrones de búsqueda para nombre y teléfono.
        """
        self.patterns = {
            'name': r"(?:mi\s+nombre\s+es|nombre\s*[:\-]?)\s*([A-Za-zÁÉÍÓÚáéíóúÑñ\s]+)",
            'phone': r"(?:mi\s+número\s+de\s+tel[eé]fono\s+es|tel[eé]fono\s*[:\-]?)\s*(\+?\d[\d\s\-]{6,15})"
        }

    def extract(self, text: str) -> Dict[str, Optional[str]]:
        """
        Extrae nombre y teléfono del texto del usuario.
        
        Args:
        - text (str): Entrada del usuario.
        
        Returns:
        - dict: Con las claves 'name' y 'phone', si fueron encontrados.
        """
        extracted_info: Dict[str, Optional[str]] = {
            'name': None,
            'phone': None
        }

        # Buscar nombre
        name_match = re.search(self.patterns['name'], text, re.IGNORECASE)
        if name_match:
            extracted_info['name'] = name_match.group(1).strip()

        # Buscar teléfono
        phone_match = re.search(self.patterns['phone'], text, re.IGNORECASE)
        if phone_match:
            extracted_info['phone'] = re.sub(r"[^\d+]", "", phone_match.group(1).strip())  # Limpia espacios o guiones

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
        if not extracted_info['phone']:
            missing.append("tu número de teléfono")

        if missing:
            return f"Para continuar necesito {', y '.join(missing)}. ¿Podrías proporcionármelos por favor?"

        return "✅ ¡Gracias por la información! Ahora dime, ¿en qué puedo ayudarte?"
