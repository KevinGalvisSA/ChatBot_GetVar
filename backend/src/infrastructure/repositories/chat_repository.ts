// src/domain/repositories/chat_repository.ts
import { AppDataSource } from '../../config/data_source';
import { Chat } from '../..//domain/entities/chat_entity';
import { Repository } from 'typeorm';

export class ChatRepository {
  private repo: Repository<Chat>;

  constructor() {
    this.repo = AppDataSource.getRepository(Chat);
  }

  // ✅ Buscar un chat por ID
  async findById(id: number): Promise<Chat | null> {
    return await this.repo.findOne({ where: { id }, relations: ['customer'] });
  }

  // ✅ Buscar por customerId (como validación previa a crear)
  async findByCustomerId(customerId: number): Promise<Chat | null> {
    return await this.repo.findOne({ where: { customerId } });
  }

  // ✅ Crear nuevo chat
  async create(chatData: Partial<Chat>): Promise<Chat> {
    const newChat = this.repo.create(chatData);
    return await this.repo.save(newChat);
  }

  // ✅ Actualizar chat existente
  async update(id: number, updateData: Partial<Chat>): Promise<Chat> {
    const chat = await this.findById(id);
    if (!chat) throw new Error('Chat no encontrado');
    Object.assign(chat, updateData);
    return await this.repo.save(chat);
  }

  // ✅ Eliminar un chat (opcional)
  async delete(id: number): Promise<void> {
    const result = await this.repo.delete(id);
    if (result.affected === 0) {
      throw new Error('Chat no encontrado para eliminar');
    }
  }

  // ✅ Listar todos los chats (opcional)
  async findAll(): Promise<Chat[]> {
    return await this.repo.find({ relations: ['customer'] });
  }
}
