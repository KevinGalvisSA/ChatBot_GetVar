// src/application/services/chat_service.ts

import { ChatRepository } from '../../infrastructure/repositories/chat_repository';
import { Chat } from '../../domain/entities/chat_entity';

export class ChatService {
    private repo = new ChatRepository();

    async createChat(data: Partial<Chat>) {
        return this.repo.create(data);
    }

    async getChatsByCustomer(customerId: number) {
        return this.repo.findByCustomerId(customerId);
    }

    async getAllChats() {
        return this.repo.findAll();
    }

    async updateChat(id: number, data: Partial<Chat>) {
        return this.repo.update(id, data);
    }

    async deleteChat(id: number) {
        return this.repo.delete(id);
    }
}
