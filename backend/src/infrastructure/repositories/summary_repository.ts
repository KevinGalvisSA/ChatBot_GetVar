// backend/src/infrastructure/repositories/summary.repository.ts
import { AppDataSource } from '../../config/data-source';
import { Summary } from '../../domain/entities/summary_entity';

export class SummaryRepository {
    private repo = AppDataSource.getRepository(Summary);

    async save(userId: string, content: string) {
        const summary = this.repo.create({ userId, content });
        return await this.repo.save(summary);
    }

    async getLatest(userId: string) {
        return await this.repo.findOne({
            where: { userId },
            order: { createdAt: 'DESC' }
        });
    }
}
