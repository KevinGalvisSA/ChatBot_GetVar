// src/infrastructure/repositories/messageStorage_repository.ts

import { AppDataSource } from '../../config/data_source';
import { MessageStorage } from '../../domain/entities/messageStorage_entity';

export class MessageStorageRepository {
    private repo = AppDataSource.getRepository(MessageStorage);

    // Crear un registro de MessageStorage
    async create(data: Partial<MessageStorage>) {
        const storage = this.repo.create(data);
        return this.repo.save(storage);
    }

    // Buscar registros por customerId
    async findByCustomerId(customerId: number) {
        return this.repo.find({
            where: { customerId },
        });
    }

    // Obtener todos los registros
    async findAll() {
        return this.repo.find();
    }

    // Actualizar un registro
    async update(id: number, data: Partial<MessageStorage>) {
        await this.repo.update(id, data);
        return this.repo.findOneBy({ id });
    }

    // Eliminar un registro
    async delete(id: number) {
        const storage = await this.repo.findOneBy({ id });
        if (storage) {
            return this.repo.remove(storage);
        }
        return null;
    }
}
