import { Chat } from '../../domain/entities/chat_entity';
import { ChatRepository } from '../../infrastructure/repositories/chat_repository';
import axios from 'axios';

export class ChatService {
    private chatRepository: ChatRepository;

    constructor() {
        this.chatRepository = new ChatRepository();
    }

    async createChatIfNotExists(customerId: number): Promise<Chat> {
        const existing = await this.chatRepository.findByCustomerId(customerId);
        if (existing) return existing;

        const chat = await this.chatRepository.create({
            customerId,
            lastConnection: new Date(),
            createdBy: customerId,
            updatedBy: customerId,
        });

        return chat;
    }

    async getChatById(id: number): Promise<Chat> {
        const chat = await this.chatRepository.findById(id);
        if (!chat) throw new Error('Chat no encontrado');
        return chat;
    }

    async getChatByCustomerId(customerId: number): Promise<Chat> {
        const chat = await this.chatRepository.findByCustomerId(customerId);
        if (!chat) throw new Error('El cliente no tiene un chat asociado');
        return chat;
    }

    async updateChat(id: number, updates: Partial<Chat>): Promise<Chat> {
        return await this.chatRepository.update(id, updates);
    }

    async deleteChat(id: number): Promise<void> {
        await this.chatRepository.delete(id);
    }

    async listChats(): Promise<Chat[]> {
        return await this.chatRepository.findAll();
    }

    // 🆕 NUEVA FUNCIÓN: actualizar solo el estado y generar resumen si se pone inactivo
    async updateChatState(id: number, newState: number): Promise<Chat> {
        const chat = await this.chatRepository.findById(id);
        if (!chat) throw new Error('Chat no encontrado');

        // Si ya está en el mismo estado, no hacemos nada
        if (chat.state === newState) return chat;

        const updatedChat = await this.chatRepository.updateState(id, newState);

        if (newState === 0) {
            try {
                const resumenResponse = await axios.get(
                    `http://localhost:8000/chat`
                );
                const resumen = resumenResponse.data;
                console.log('📝 Resumen generado:', resumen);

                // Puedes guardar el resumen si tienes una tabla/resumen_entity
                // o enviarlo por socket, etc.

            } catch (error) {
                console.error('❌ Error al solicitar resumen al bot:', error);
            }
        }

        return updatedChat;
    }
}
