// backend/src/infrastructure/repositories/message_storage_repository.ts

import { AppDataSource } from '../../config/data_source';
import { Repository } from 'typeorm';
import { MessageStorage } from '../../domain/entities/messageStorage_entity';

export class MessageStorageRepository {
    private repository: Repository<MessageStorage>;

    constructor() {
        this.repository = AppDataSource.getRepository(MessageStorage);
    }

    async create(data: Partial<MessageStorage>): Promise<MessageStorage> {
        const storage = this.repository.create(data);
        return await this.repository.save(storage);
    }

    async findByCustomerId(customerId: number): Promise<MessageStorage | null> {
        return await this.repository.findOne({
            where: { customerId },
            relations: ['customer'],
        });
    }

    async findBySessionId(sessionId: number): Promise<MessageStorage | null> {
        return await this.repository.findOne({
            where: { sessionId },
            relations: ['customer'],
        });
    }

    async deleteByCustomerId(customerId: number): Promise<boolean> {
        const result = await this.repository.delete({ customerId });
        return result.affected !== 0;
    }

    async clear(): Promise<void> {
        await this.repository.clear();
    }
}
