// backend/src/application/services/customer_service.ts

import { CustomerRepository } from '../../infrastructure/repositories/customer_repository';
import { Customer } from '../../domain/entities/customer_entity';

export class CustomerService {
    private customerRepository: CustomerRepository;

    constructor() {
        this.customerRepository = new CustomerRepository();
    }

    async getCustomer(name: null | string, phone: number, company: string | null, rol: string | null,): Promise<Customer> {
        const existing = await this.customerRepository.findByphone(phone);
        if (existing) return existing;

        return await this.customerRepository.create({ name, phone, company, rol });
    }

    async updateCustomer(id: number, data: Partial<Customer>): Promise<Customer | null> {
        return await this.customerRepository.update(id, data);
    }

    async deleteCustomer(id: number): Promise<boolean> {
        return await this.customerRepository.delete(id);
    }

    async getCustomerById(id: number): Promise<Customer | null> {
        return await this.customerRepository.findById(id);
    }

    async getCustomerByphone(phone: number): Promise<Customer | null> {
        return await this.customerRepository.findByphone(phone);
    }
}

