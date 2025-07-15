// src/adapters/http/controllers/customer_controller.ts

import { Request, Response } from 'express';
import { CustomerService } from '../../../application/services/customer_service';

const service = new CustomerService();

export const createCustomer = async (req: Request, res: Response) => {
    const customer = await service.registerCustomer(req.body);
    return res.status(201).json(customer);
};

export const getCustomer = async (req: Request, res: Response) => {
    const customer = await service.getCustomerById(Number(req.params.id));
    return res.json(customer);
};

export const getAllCustomers = async (_: Request, res: Response) => {
    const customers = await service.listAllCustomers();
    return res.json(customers);
};

export const updateCustomer = async (req: Request, res: Response) => {
    const updated = await service.updateCustomer(Number(req.params.id), req.body);
    return res.json(updated);
};

export const deleteCustomer = async (req: Request, res: Response) => {
    const deleted = await service.removeCustomer(Number(req.params.id));
    return res.json(deleted);
};
