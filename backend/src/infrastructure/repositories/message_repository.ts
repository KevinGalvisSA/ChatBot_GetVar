// backend/src/infrastructure/repositories/message.repository.ts
import { AppDataSource } from '../../config/data-source';
import { Message } from '../../domain/entities/message_entity';

export class MessageRepository {
    private repo = AppDataSource.getRepository(Message);

    async save(userId: string, role: 'user' | 'bot', content: string) {
        const message = this.repo.create({ userId, role, content });
        return await this.repo.save(message);
    }

    async getHistory(userId: string) {
        return await this.repo.find({
            where: { userId },
            order: { createdAt: 'ASC' }
        });
    }
}
