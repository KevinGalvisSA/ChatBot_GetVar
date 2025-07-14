// backend/src/application/services/message.service.ts
import { MessageRepository } from '../../infrastructure/repositories/message_repository';

export class MessageService {
    constructor(private readonly repo = new MessageRepository()) { }

    async saveUserMessage(userId: string, content: string) {
        return this.repo.save(userId, 'user', content);
    }

    async saveBotMessage(userId: string, content: string) {
        return this.repo.save(userId, 'bot', content);
    }

    async getConversation(userId: string) {
        return this.repo.getHistory(userId);
    }
}
