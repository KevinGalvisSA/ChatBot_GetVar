// backend/src/application/services/pythonCommunication.ts

export class pythonCommunication {
    static async sendMessageToPython(
        message: string,
        session_id: string
    ): Promise<string> {
        console.log('📤 Enviando mensaje a FastAPI:', message);

        try {
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message, session_id }),
            });

            if (!response.ok) {
                throw new Error('Error en la respuesta de FastAPI');
            }

            const data = await response.json();
            console.log('📥 Respuesta recibida de FastAPI:', data);
            return data.response;
        } catch (error) {
            console.error('❌ Error al llamar a FastAPI:', error);
            throw error;
        }
    }

    static async generateSummary(chat_id: number, session_id: string): Promise<string> {
        console.log('📤 Solicitando resumen a FastAPI para chat:', chat_id, session_id);

        try {
            const response = await fetch('http://localhost:8000/resumen', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    message: "no se usa",
                    session_id,
                    chat_id
                }),
            });

            if (!response.ok) {
                throw new Error('Error en la respuesta de FastAPI resumen');
            }

            const data = await response.json();
            console.log('📥 Resumen recibido desde FastAPI:', data);
            return data.resumen;
        } catch (error) {
            console.error('❌ Error al generar resumen:', error);
            throw error;
        }
    }
}
