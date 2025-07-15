// src/application/services/customer_service.ts

import { CustomerRepository } from '../../infrastructure/repositories/customer_repository';
import { Customer } from '../../domain/entities/customer_entity';

export class CustomerService {
    private repo = new CustomerRepository();

    async registerCustomer(data: Partial<Customer>) {
        return this.repo.create(data);
    }

    async getCustomerById(id: number) {
        return this.repo.findById(id);
    }

    async listAllCustomers() {
        return this.repo.findAll();
    }

    async updateCustomer(id: number, data: Partial<Customer>) {
        return this.repo.update(id, data);
    }

    async removeCustomer(id: number) {
        return this.repo.delete(id);
    }
}
