// backend/src/domain/services/chat_service.ts
import { Chat } from '../../domain/entities/chat_entity';
import { ChatRepository } from '../../infrastructure/repositories/chat_repository';

export class ChatService {
    private chatRepository: ChatRepository;

    constructor() {
        this.chatRepository = new ChatRepository();
    }

    // Crear un chat (solo si no existe ya uno para el cliente)
    async createChatIfNotExists(customerId: number): Promise<Chat> {
        const existing = await this.chatRepository.findByCustomerId(customerId);
        if (existing) return existing;

        const chat = await this.chatRepository.create({
            customerId,
            lastConnection: new Date(),
            createdBy: customerId,
            updatedBy: customerId,
        });q

        return chat;
    }

    // Obtener chat por ID
    async getChatById(id: number): Promise<Chat> {
        const chat = await this.chatRepository.findById(id);
        if (!chat) throw new Error('Chat no encontrado');
        return chat;
    }

    // Obtener chat por ID de cliente
    async getChatByCustomerId(customerId: number): Promise<Chat> {
        const chat = await this.chatRepository.findByCustomerId(customerId);
        if (!chat) throw new Error('El cliente no tiene un chat asociado');
        return chat;
    }

    // Actualizar datos del chat
    async updateChat(id: number, updates: Partial<Chat>): Promise<Chat> {
        return await this.chatRepository.update(id, updates);
    }

    // Eliminar un chat (opcional)
    async deleteChat(id: number): Promise<void> {
        await this.chatRepository.delete(id);
    }

    // Listar todos los chats (opcional)
    async listChats(): Promise<Chat[]> {
        return await this.chatRepository.findAll();
    }
}
