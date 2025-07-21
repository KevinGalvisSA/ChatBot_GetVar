// backend/src/adapters/http/controllers/messageStorage_controller.ts

import { Request, Response } from 'express';
import { MessageStorageService } from '../../../application/services/messageStorage_service';
import { ApiResponse } from '../../../handleUtils/apiResponse';

const messageStorageService = new MessageStorageService();

export class MessageStorageController {
    static async create(req: Request, res: Response) {
        try {
            const data = req.body;
            const created = await messageStorageService.createStorageMessage(data);
            return ApiResponse.created(res, 'Mensaje almacenado correctamente', created);
        } catch (error) {
            return ApiResponse.error(res, error);
        }
    }

    static async getByCustomerId(req: Request, res: Response) {
        try {
            const customerId = parseInt(req.params.customerId);
            if (isNaN(customerId)) {
                return ApiResponse.badRequest(res, 'Parámetro customerId inválido');
            }

            const record = await messageStorageService.getByCustomerId(customerId);
            if (!record) {
                return ApiResponse.notFound(res, 'No se encontró almacenamiento para este cliente');
            }

            return ApiResponse.success(res, 'Mensaje encontrado', record);
        } catch (error) {
            return ApiResponse.error(res, error);
        }
    }

    static async getBySessionId(req: Request, res: Response) {
        try {
            const sessionId = BigInt(req.params.sessionId);
            const record = await messageStorageService.getBySessionId(sessionId);
            if (!record) {
                return ApiResponse.notFound(res, 'No se encontró almacenamiento para esta sesión');
            }

            return ApiResponse.success(res, 'Mensaje encontrado', record);
        } catch (error) {
            return ApiResponse.error(res, error);
        }
    }

    static async deleteByCustomerId(req: Request, res: Response) {
        try {
            const customerId = parseInt(req.params.customerId);
            if (isNaN(customerId)) {
                return ApiResponse.badRequest(res, 'Parámetro customerId inválido');
            }

            const deleted = await messageStorageService.deleteByCustomerId(customerId);
            if (!deleted) {
                return ApiResponse.notFound(res, 'No se encontró mensaje para eliminar');
            }

            return ApiResponse.success(res, 'Mensaje eliminado correctamente');
        } catch (error) {
            return ApiResponse.error(res, error);
        }
    }
}
