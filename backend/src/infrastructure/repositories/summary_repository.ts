// backend/src/infrastructure/repositories/resumen_repository.ts

import { AppDataSource } from '../../config/data_source';
import { Summary } from '../../domain/entities/summary_entity';
import { Repository } from 'typeorm';

export class SummaryRepository {
    private repo: Repository<Summary>;

    constructor() {
        this.repo = AppDataSource.getRepository(Summary);
    }

    async create(data: Partial<Summary>): Promise<Summary> {
        const resumen = this.repo.create(data);
        return await this.repo.save(resumen);
    }

    async findBychat_id(chat_id: number): Promise<Summary[]> {
        return await this.repo.find({ where: { chat_id } });
    }
}
