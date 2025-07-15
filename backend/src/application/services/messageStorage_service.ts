// src/application/services/messageStorage_service.ts

import { MessageStorageRepository } from '../../infrastructure/repositories/messageStorage_repository';
import { MessageStorage } from '../../domain/entities/messageStorage_entity';

export class MessageStorageService {
  private repo = new MessageStorageRepository();

  async createMessageStorage(data: Partial<MessageStorage>) {
    return this.repo.create(data);
  }

  async getStorageByCustomer(customerId: number) {
    return this.repo.findByCustomerId(customerId);
  }

  async getAllStorages() {
    return this.repo.findAll();
  }

  async updateStorage(id: number, data: Partial<MessageStorage>) {
    return this.repo.update(id, data);
  }

  async deleteStorage(id: number) {
    return this.repo.delete(id);
  }
}
