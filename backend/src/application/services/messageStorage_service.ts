// backend/src/application/services/message_storage_service.ts

import { MessageStorageRepository } from '../../infrastructure/repositories/messageStorage_repository';
import { MessageStorage } from '../../domain/entities/messageStorage_entity';

export class MessageStorageService {
  private messageStorageRepository: MessageStorageRepository;

  constructor() {
    this.messageStorageRepository = new MessageStorageRepository();
  }

  async createStorageMessage(data: Partial<MessageStorage>): Promise<MessageStorage> {
    if (!data.customer || !data.id_customer) {
      throw new Error('Customer relation is required.');
    }

    if (!data.session_id) {
      throw new Error('Session ID is required.');
    }

    if (!data.message || data.message.trim() === '') {
      throw new Error('Message content cannot be empty.');
    }

    if (!data.message_type) {
      throw new Error('Message type is required.');
    }

    return await this.messageStorageRepository.create(data);
  }

  async getByid_customer(id_customer: number): Promise<MessageStorage | null> {
    return await this.messageStorageRepository.findByid_customer(id_customer);
  }

  async getBysession_id(session_id: number): Promise<MessageStorage | null> {
    return await this.messageStorageRepository.findBysession_id(session_id);
  }

  async deleteByid_customer(id_customer: number): Promise<boolean> {
    return await this.messageStorageRepository.deleteByid_customer(id_customer);
  }
}
