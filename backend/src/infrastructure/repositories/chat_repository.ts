import { AppDataSource } from '../../config/data_source';
import { Chat } from '../../domain/entities/chat_entity';

export class ChatRepository {
    private repo = AppDataSource.getRepository(Chat);

    // Crear un chat
    async create(chat: Partial<Chat>) {
        const newChat = this.repo.create(chat);
        return this.repo.save(newChat);
    }

    // Buscar chat por customerId
    async findByCustomerId(customerId: number) {
        return this.repo.find({
            where: { customerId }, // Filtramos por customerId
        });
    }

    // Obtener todos los chats
    async findAll() {
        return this.repo.find();
    }

    // Actualizar chat
    async update(id: number, chat: Partial<Chat>) {
        await this.repo.update(id, chat);
        return this.repo.findOneBy({ id });
    }

    // Eliminar un chat
    async delete(id: number) {
        const chat = await this.repo.findOneBy({ id });
        if (chat) {
            return this.repo.remove(chat);
        }
        return null;
    }
}
