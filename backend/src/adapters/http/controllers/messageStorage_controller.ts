// backend/src/adapters/http/controllers/messageStorage_controller.ts

import { Request, Response } from 'express';
import { MessageStorageService } from '../../../application/services/messageStorage_service';
import { ApiResponse } from '../../../handleUtils/apiResponse';

const service = new MessageStorageService();

export const createMessageStorageData = async (req: Request, res: Response) => {
    try {
        const result = await service.createMessageStorage(req.body);
        return ApiResponse.created(res, 'Almacenamiento de mensaje creado exitosamente', result);
    } catch (error) {
        return ApiResponse.internalServerError(res, 'Error al crear almacenamiento de mensaje');
    }
};

export const getStorageDataByCustomer = async (req: Request, res: Response) => {
    try {
        const storages = await service.getStorageByCustomer(Number(req.params.customerId));
        if (!storages || storages.length === 0) {
            return ApiResponse.notFound(res, 'No se encontraron datos de almacenamiento para este cliente');
        }
        return ApiResponse.success(res, 'Datos de almacenamiento encontrados', storages);
    } catch (error) {
        return ApiResponse.internalServerError(res, 'Error al obtener datos de almacenamiento');
    }
};

export const getAllStoragesData = async (_: Request, res: Response) => {
    try {
        const storages = await service.getAllStorages();
        return ApiResponse.success(res, 'Datos de almacenamiento encontrados', storages);
    } catch (error) {
        return ApiResponse.internalServerError(res, 'Error al obtener todos los datos de almacenamiento');
    }
};

export const updateStorageData = async (req: Request, res: Response) => {
    try {
        const updated = await service.updateStorage(Number(req.params.id), req.body);
        if (!updated) {
            return ApiResponse.notFound(res, 'Almacenamiento de mensaje no encontrado para actualizar');
        }
        return ApiResponse.success(res, 'Almacenamiento de mensaje actualizado exitosamente', updated);
    } catch (error) {
        return ApiResponse.internalServerError(res, 'Error al actualizar almacenamiento de mensaje');
    }
};

export const deleteStorageData = async (req: Request, res: Response) => {
    try {
        const deleted = await service.deleteStorage(Number(req.params.id));
        if (!deleted) {
            return ApiResponse.notFound(res, 'Almacenamiento de mensaje no encontrado para eliminar');
        }
        return ApiResponse.success(res, 'Almacenamiento de mensaje eliminado exitosamente', deleted);
    } catch (error) {
        return ApiResponse.internalServerError(res, 'Error al eliminar almacenamiento de mensaje');
    }
};
