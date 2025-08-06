// backend/src/adapters/http/controllers/customer_controller.ts

import { Request, Response } from 'express';
import { ApiResponse } from '../../../handleUtils/apiResponse';
import { CustomerService } from '../../../application/services/customer_service';

const customerService = new CustomerService();

export class CustomerController {
    static async getOrCreate(req: Request, res: Response) {
        try {
            const { name, phone, company, rol } = req.body;

            if (!phone || isNaN(Number(phone))) {
                return ApiResponse.badRequest(res, 'El campo phone es obligatorio y debe ser numérico');
            }

            if (company !== null && typeof company !== 'string') {
                return ApiResponse.badRequest(res, 'El campo company debe ser un string')
            }

            if (rol !== null && typeof rol !== 'string'){
                return ApiResponse.badRequest(res, 'El campo rol debe ser un string')
            }

            const customer = await customerService.getCustomer(name, Number(phone), company, rol);
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

    static async getByphone(req: Request, res: Response) {
        try {
            const phone = Number(req.params.phone);
            if (isNaN(phone)) return ApiResponse.badRequest(res, 'Teléfono inválido');

            const customer = await customerService.getCustomerByphone(phone);
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
