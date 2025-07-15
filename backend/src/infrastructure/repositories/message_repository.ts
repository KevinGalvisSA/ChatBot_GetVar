// src/infrastructure/repositories/message_repository.ts

import { AppDataSource } from '../../config/data_source';
import { Message } from '../../domain/entities/message_entity';

export class MessageRepository {
    private repo = AppDataSource.getRepository(Message);

    // Crear un mensaje
    async create(message: Partial<Message>) {
        const newMsg = this.repo.create(message);
        return this.repo.save(newMsg);
    }

    // Buscar mensajes por chatId
    async findByChatId(chatId: number) {
        return this.repo.find({
            where: { chatId }, // Filtramos por chatId
        });
    }

    // Obtener todos los mensajes
    async findAll() {
        return this.repo.find();
    }

    // Actualizar un mensaje
    async update(id: number, message: Partial<Message>) {
        await this.repo.update(id, message);
        return this.repo.findOneBy({ id });
    }

    // Eliminar un mensaje
    async delete(id: number) {
        const message = await this.repo.findOneBy({ id });
        if (message) {
            return this.repo.remove(message);
        }
        return null;
    }
}
