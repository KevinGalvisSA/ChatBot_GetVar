// backend/src/application/services/pythonCommunication.ts

export class pythonCommunication {
    static async sendMessageToPython(message: string): Promise<string> {
        console.log('Enviando mensaje a FastAPI:', message);

        try {
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message }),
            });

            if (!response.ok) {
                throw new Error('Error en la respuesta de FastAPI');
            }

            const data = await response.json();
            console.log('Respuesta recibida de FastAPI:', data);
            return data.response;
        } catch (error) {
            console.error('Error al llamar a FastAPI:', error);
            throw error;
        }
    }
}
