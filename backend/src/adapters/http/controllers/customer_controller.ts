// backend/src/adapters/http/controllers/customer_controller.ts

import { Request, Response } from 'express';
import { CustomerService } from '../../../application/services/customer_service';
import { ApiResponse } from '../../../handleUtils/apiResponse';

const service = new CustomerService();

export const createCustomer = async (req: Request, res: Response) => {
    try {
        const customer = await service.registerCustomer(req.body);
        return ApiResponse.created(res, 'Cliente creado exitosamente', customer);  
    } catch (error) {
        return ApiResponse.internalServerError(res, 'Error al crear el cliente'); 
    }
};

export const getCustomer = async (req: Request, res: Response) => {
    try {
        const customer = await service.getCustomerById(Number(req.params.id));
        if (!customer) {
            return ApiResponse.notFound(res, 'Cliente no encontrado');  
        }
        return ApiResponse.success(res, 'Cliente encontrado', customer);  
    } catch (error) {
        return ApiResponse.internalServerError(res, 'Error al obtener el cliente'); 
    }
};

export const getAllCustomers = async (_: Request, res: Response) => {
    try {
        const customers = await service.listAllCustomers();
        return ApiResponse.success(res, 'Clientes encontrados', customers);  
    } catch (error) {
        return ApiResponse.internalServerError(res, 'Error al obtener los clientes'); 
    }
};

export const updateCustomer = async (req: Request, res: Response) => {
    try {
        const updated = await service.updateCustomer(Number(req.params.id), req.body);
        if (!updated) {
            return ApiResponse.notFound(res, 'Cliente no encontrado para actualizar');  
        }
        return ApiResponse.success(res, 'Cliente actualizado exitosamente', updated);  
    } catch (error) {
        return ApiResponse.internalServerError(res, 'Error al actualizar el cliente'); 
    }
};

export const deleteCustomer = async (req: Request, res: Response) => {
    try {
        const deleted = await service.removeCustomer(Number(req.params.id));
        if (!deleted) {
            return ApiResponse.notFound(res, 'Cliente no encontrado para eliminar');  
        }
        return ApiResponse.success(res, 'Cliente eliminado exitosamente', deleted);  
    } catch (error) {
        return ApiResponse.internalServerError(res, 'Error al eliminar el cliente'); 
    }
};
