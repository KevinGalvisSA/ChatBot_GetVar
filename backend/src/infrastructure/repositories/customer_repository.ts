// backend/src/infrastructure/repositories/customer_repository.ts

import { AppDataSource } from '../../config/data_source';
import { Customer } from '../../domain/entities/customer_entity';
import { Repository } from 'typeorm';

export class CustomerRepository {
    private repository: Repository<Customer>;

    constructor() {
        this.repository = AppDataSource.getRepository(Customer);
    }

    async findById(id: number): Promise<Customer | null> {
        return await this.repository.findOne({ where: { id } });
    }

    async findByPhone(phone: number): Promise<Customer | null> {
        return await this.repository.findOne({ where: { phone } });
    }

    async create(customerData: Partial<Customer>): Promise<Customer> {
        const customer = this.repository.create(customerData);
        return await this.repository.save(customer);
    }

    async update(id: number, data: Partial<Customer>): Promise<Customer | null> {
        const customer = await this.findById(id);
        if (!customer) return null;
        Object.assign(customer, data);
        return await this.repository.save(customer);
    }

    async delete(id: number): Promise<boolean> {
        const result = await this.repository.delete(id);
        return result.affected !== 0;
    }
}
