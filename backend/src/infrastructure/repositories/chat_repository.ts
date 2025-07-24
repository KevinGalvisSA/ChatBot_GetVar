// backend/src/domain/repositories/chat_repository.ts
import { AppDataSource } from '../../config/data_source';
import { Chat } from '../..//domain/entities/chat_entity';
import { Repository, LessThan } from 'typeorm';

export class ChatRepository {
  private repo: Repository<Chat>;

  constructor() {
    this.repo = AppDataSource.getRepository(Chat);
  }

  async findById(id: number): Promise<Chat | null> {
    return await this.repo.findOne({ where: { id }, relations: ['customer'] });
  }

  async findByid_customer(id_customer: number): Promise<Chat | null> {
    return await this.repo.findOne({ where: { id_customer } });
  }

  async getInactiveSince(threshold: Date): Promise<Chat[]> {
    return await this.repo.find({
      where: {
        state: 1,
        last_connection: LessThan(threshold),
      },
    });
  }


  async create(chatData: Partial<Chat>): Promise<Chat> {
    const newChat = this.repo.create(chatData);
    return await this.repo.save(newChat);
  }

  async update(id: number, updateData: Partial<Chat>): Promise<Chat> {
    const chat = await this.findById(id);
    if (!chat) throw new Error('Chat no encontrado');
    Object.assign(chat, updateData);
    return await this.repo.save(chat);
  }

  async delete(id: number): Promise<void> {
    const result = await this.repo.delete(id);
    if (result.affected === 0) {
      throw new Error('Chat no encontrado para eliminar');
    }
  }

  async findAll(): Promise<Chat[]> {
    return await this.repo.find({ relations: ['customer'] });
  }

  // 🆕 NUEVA FUNCIÓN: actualizar sólo el estado del chat
  async updateState(id: number, newState: number): Promise<Chat> {
    const chat = await this.findById(id);
    if (!chat) throw new Error('Chat no encontrado');

    chat.state = newState;
    return await this.repo.save(chat);
  }
}

