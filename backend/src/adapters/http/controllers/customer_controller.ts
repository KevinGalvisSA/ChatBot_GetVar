// backend/src/adapters/http/controllers/customer_controller.ts

import { Request, Response } from 'express';
import { ApiResponse } from '../../../handleUtils/apiResponse';
import { CustomerService } from '../../../application/services/customer_service';

const customerService = new CustomerService();

export class CustomerController {
    static async getOrCreate(req: Request, res: Response) {
        try {
            const { name, phone_number } = req.body;

            if (!name || typeof name !== 'string' || name.trim() === '') {
                return ApiResponse.badRequest(res, 'El nombre es obligatorio y debe ser una cadena no vacía');
            }

            if (!phone_number || isNaN(Number(phone_number))) {
                return ApiResponse.badRequest(res, 'El teléfono es obligatorio y debe ser numérico');
            }

            const customer = await customerService.getOrCreateCustomer(name, Number(phone_number));
            return ApiResponse.success(res, 'Cliente obtenido o creado correctamente', customer);
        } catch (error) {
            return ApiResponse.error(res, error);
        }
    }

    static async getById(req: Request, res: Response) {
        try {
            const id = parseInt(req.params.id);
            if (isNaN(id)) return ApiResponse.badRequest(res, 'ID inválido');

            const customer = await customerService.getCustomerById(id);
            if (!customer) return ApiResponse.notFound(res, 'Cliente no encontrado');

            return ApiResponse.success(res, 'Cliente obtenido correctamente', customer);
        } catch (error) {
            return ApiResponse.error(res, error);
        }
    }

    static async getByphone_number(req: Request, res: Response) {
        try {
            const phone_number = Number(req.params.phone_number);
            if (isNaN(phone_number)) return ApiResponse.badRequest(res, 'Teléfono inválido');

            const customer = await customerService.getCustomerByphone_number(phone_number);
            if (!customer) return ApiResponse.notFound(res, 'Cliente no encontrado');

            return ApiResponse.success(res, 'Cliente obtenido correctamente', customer);
        } catch (error) {
            return ApiResponse.error(res, error);
        }
    }

    static async update(req: Request, res: Response) {
        try {
            const id = parseInt(req.params.id);
            if (isNaN(id)) return ApiResponse.badRequest(res, 'ID inválido');

            const updated = await customerService.updateCustomer(id, req.body);
            if (!updated) return ApiResponse.notFound(res, 'Cliente no encontrado para actualizar');

            return ApiResponse.success(res, 'Cliente actualizado correctamente', updated);
        } catch (error) {
            return ApiResponse.error(res, error);
        }
    }

    static async delete(req: Request, res: Response) {
        try {
            const id = parseInt(req.params.id);
            if (isNaN(id)) return ApiResponse.badRequest(res, 'ID inválido');

            const deleted = await customerService.deleteCustomer(id);
            if (!deleted) return ApiResponse.notFound(res, 'Cliente no encontrado para eliminar');

            return ApiResponse.success(res, 'Cliente eliminado correctamente');
        } catch (error) {
            return ApiResponse.error(res, error);
        }
    }
}
