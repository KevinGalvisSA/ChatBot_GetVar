// backend/src/infrastructure/repositories/message_repository.ts

import { AppDataSource } from '../../config/data_source';
import { Repository } from 'typeorm';
import { Message } from '../../domain/entities/message_entity';

export class MessageRepository {
    private repository: Repository<Message>;

    constructor() {
        this.repository = AppDataSource.getRepository(Message);
    }

    async create(messageData: Partial<Message>): Promise<Message> {
        const message = this.repository.create(messageData);
        return await this.repository.save(message);
    }

    async findById(id: number): Promise<Message | null> {
        return await this.repository.findOne({ where: { id }, relations: ['chat'] });
    }

    async getAllByChatId(chatId: number): Promise<Message[]> {
        return await this.repository.find({
            where: { chat: { id: chatId } },
            relations: ['chat'],
            order: { createdAt: 'ASC' },
        });
    }

    async deleteById(id: number): Promise<boolean> {
        const result = await this.repository.delete(id);
        return result.affected !== 0;
    }
}
