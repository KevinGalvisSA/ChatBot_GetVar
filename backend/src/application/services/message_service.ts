// src/application/services/message_service.ts

import { MessageRepository } from '../../infrastructure/repositories/message_repository';
import { Message } from '../../domain/entities/message_entity';

export class MessageService {
    private repo = new MessageRepository();

    async createMessage(data: Partial<Message>) {
        return this.repo.create(data);
    }

    async getMessagesByChat(chatId: number) {
        return this.repo.findByChatId(chatId);
    }

    async getAllMessages() {
        return this.repo.findAll();
    }

    async updateMessage(id: number, data: Partial<Message>) {
        return this.repo.update(id, data);
    }

    async deleteMessage(id: number) {
        return this.repo.delete(id);
    }
}
