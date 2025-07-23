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

    async findByid_customer(id_customer: number): Promise<MessageStorage | null> {
        return await this.repository.findOne({
            where: { id_customer },
            relations: ['customer'],
        });
    }

    async findBysession_id(session_id: number): Promise<MessageStorage | null> {
        return await this.repository.findOne({
            where: { session_id },
            relations: ['customer'],
        });
    }

    async deleteByid_customer(id_customer: number): Promise<boolean> {
        const result = await this.repository.delete({ id_customer });
        return result.affected !== 0;
    }

    async clear(): Promise<void> {
        await this.repository.clear();
    }
}
