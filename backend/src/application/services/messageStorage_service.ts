// backend/src/application/services/message_storage_service.ts

import { MessageStorageRepository } from '../../infrastructure/repositories/messageStorage_repository';
import { MessageStorage } from '../../domain/entities/messageStorage_entity';

export class MessageStorageService {
  private messageStorageRepository: MessageStorageRepository;

  constructor() {
    this.messageStorageRepository = new MessageStorageRepository();
  }

  async createStorageMessage(data: Partial<MessageStorage>): Promise<MessageStorage> {
    if (!data.customer || !data.customerId) {
      throw new Error('Customer relation is required.');
    }

    if (!data.sessionId) {
      throw new Error('Session ID is required.');
    }

    if (!data.message || data.message.trim() === '') {
      throw new Error('Message content cannot be empty.');
    }

    if (!data.messageType) {
      throw new Error('Message type is required.');
    }

    return await this.messageStorageRepository.create(data);
  }

  async getByCustomerId(customerId: number): Promise<MessageStorage | null> {
    return await this.messageStorageRepository.findByCustomerId(customerId);
  }

  async getBySessionId(sessionId: number): Promise<MessageStorage | null> {
    return await this.messageStorageRepository.findBySessionId(sessionId);
  }

  async deleteByCustomerId(customerId: number): Promise<boolean> {
    return await this.messageStorageRepository.deleteByCustomerId(customerId);
  }
}
