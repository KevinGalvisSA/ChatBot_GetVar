// backend/src/application/services/pythonCommunication.ts

export class pythonCommunication {
    static async sendMessageToPython(message: string, id_session: string): Promise<string> {
        console.log('📤 Enviando mensaje a FastAPI:', message);

        try {
            const response = await fetch('http://localhost:8000/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message, id_session }),
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

    // 🆕 Nueva función para resumen
    static async generateSummary(chatId: number, id_session: string): Promise<string> {
        console.log('📤 Solicitando resumen a FastAPI para chat:', chatId);

        try {
            const response = await fetch('http://localhost:8000/resumen', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ chatId, id_session }),
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
