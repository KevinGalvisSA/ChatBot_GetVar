// src/infrastructure/repositories/customer_repository.ts

import { AppDataSource } from '../../config/data_source';
import { Customer } from '../../domain/entities/customer_entity';

export class CustomerRepository {
    private repo = AppDataSource.getRepository(Customer);

    // Crear un cliente
    async create(data: Partial<Customer>) {
        const customer = this.repo.create(data);
        return this.repo.save(customer);
    }

    // Buscar cliente por ID
    async findById(id: number) {
        return this.repo.findOne({
            where: { id },
        });
    }

    // Obtener todos los clientes
    async findAll() {
        return this.repo.find();
    }

    // Actualizar cliente
    async update(id: number, data: Partial<Customer>) {
        await this.repo.update(id, data);
        return this.repo.findOneBy({ id });
    }

    // Eliminar un cliente
    async delete(id: number) {
        const customer = await this.repo.findOneBy({ id });
        if (customer) {
            return this.repo.remove(customer);
        }
        return null;
    }
}
