// backend/src/application/services/message_service.ts

import { MessageRepository } from '../../infrastructure/repositories/message_repository';
import { Message } from '../../domain/entities/message_entity';

export class MessageService {
    private messageRepository: MessageRepository;

    constructor() {
        this.messageRepository = new MessageRepository();
    }

    async createMessage(data: Partial<Message>): Promise<Message> {
        if (![0, 1].includes(data.type ?? -1)) {
            throw new Error('Invalid message type. Must be 0 (user) or 1 (bot).');
        }

        if (!data.content || data.content.trim() === '') {
            throw new Error('Message content cannot be empty.');
        }

        if (!data.chat) {
            throw new Error('Chat relation is required.');
        }

        return await this.messageRepository.create(data);
    }

    async getMessagesByChat(chat_id: number): Promise<Message[]> {
        return await this.messageRepository.getAllBychat_id(chat_id);
    }

    async deleteMessage(id: number): Promise<boolean> {
        return await this.messageRepository.deleteById(id);
    }
}
