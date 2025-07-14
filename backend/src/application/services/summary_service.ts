// backend/src/application/services/summary.service.ts
import { SummaryRepository } from '../../infrastructure/repositories/summary_repository';

export class SummaryService {
    constructor(private readonly repo = new SummaryRepository()) { }

    async save(userId: string, content: string) {
        return this.repo.save(userId, content);
    }

    async getLatest(userId: string) {
        return this.repo.getLatest(userId);
    }
}
