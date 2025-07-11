import re
from typing import Dict, Optional

class InfoExtractor:
    def __init__(self):
        """
        Inicializa el extractor de información con los patrones de búsqueda.
        """
        self.patterns = {
            'name': r"([Nn]ame|[Nn]ombre)\s*[:\-]?\s*([A-Za-zÁÉÍÓÚáéíóú\s]+)",  # Extraer nombres
            'phone': r"\+?\d{1,4}[\s\-]?\(?\d{1,4}\)?[\s\-]?\d{1,4}[\s\-]?\d{1,4}",  # Extraer números de teléfono
        }

    def extract(self, text: str) -> Dict[str, Optional[str]]:
        """
        Extrae la información relevante (como nombre y teléfono) del texto.
        
        Args:
        - text (str): El texto de entrada del usuario.
        
        Returns:
        - dict: Diccionario con los campos extraídos (nombre, teléfono).
        """
        extracted_info: Dict[str, Optional[str]] = {
            'name': None,  # Tipo opcional para permitir None
            'phone': None  # Tipo opcional para permitir None
        }

        # Buscar nombre en el texto
        name_match = re.search(self.patterns['name'], text)
        if name_match:
            extracted_info['name'] = name_match.group(2).strip()  # Asignar el nombre extraído

        # Buscar teléfono en el texto
        phone_match = re.search(self.patterns['phone'], text)
        if phone_match:
            extracted_info['phone'] = phone_match.group(0).strip()  # Asignar el teléfono extraído

        return extracted_info

    def validate_extracted_info(self, extracted_info: Dict[str, Optional[str]]) -> str:
        """
        Valida si los campos extraídos son suficientes para continuar la conversación.

        Args:
        - extracted_info (dict): La información extraída (nombre, teléfono).
        
        Returns:
        - str: Mensaje que indica si falta información o si todo está listo.
        """
        if not extracted_info['name']:
            return "Parece que no me has dicho tu nombre. ¿Cómo te llamas?"
        if not extracted_info['phone']:
            return "No tengo tu número de teléfono. ¿Podrías decirme tu número?"
        return "Información completa, podemos continuar."
