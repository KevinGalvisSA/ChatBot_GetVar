// backend/src/adapters/http/controllers/message_storage_controller.ts

import { Request, Response } from 'express';
import { ApiResponse } from '../../../handleUtils/apiResponse';
import { MessageStorageService } from '../../../application/services/messageStorage_service';

const messageStorageService = new MessageStorageService();

export class MessageStorageController {
    static async create(req: Request, res: Response) {
        try {
            const data = req.body;
            const result = await messageStorageService.createStorageMessage(data);
            return ApiResponse.created(res, 'Mensaje almacenado correctamente', result);
        } catch (error) {
            return ApiResponse.error(res, error);
        }
    }

    static async getByid_customer(req: Request, res: Response) {
        try {
            const id_customer = parseInt(req.params.id_customer);
            if (isNaN(id_customer)) {
                return ApiResponse.badRequest(res, 'ID de cliente inválido');
            }

            const message = await messageStorageService.getByid_customer(id_customer);
            if (!message) {
                return ApiResponse.notFound(res, 'Mensaje no encontrado para el cliente');
            }

            return ApiResponse.success(res, 'Mensaje obtenido correctamente', message);
        } catch (error) {
            return ApiResponse.error(res, error);
        }
    }

    static async getBysession_id(req: Request, res: Response) {
        try {
            const session_id = parseInt(req.params.session_id);
            if (isNaN(session_id)) {
                return ApiResponse.badRequest(res, 'Session ID inválido');
            }

            const message = await messageStorageService.getBysession_id(session_id);
            if (!message) {
                return ApiResponse.notFound(res, 'Mensaje no encontrado para la sesión');
            }

            return ApiResponse.success(res, 'Mensaje obtenido correctamente', message);
        } catch (error) {
            return ApiResponse.error(res, error);
        }
    }

    static async deleteByid_customer(req: Request, res: Response) {
        try {
            const id_customer = parseInt(req.params.id_customer);
            if (isNaN(id_customer)) {
                return ApiResponse.badRequest(res, 'ID de cliente inválido');
            }

            const deleted = await messageStorageService.deleteByid_customer(id_customer);
            if (!deleted) {
                return ApiResponse.notFound(res, 'No se encontró un mensaje para eliminar');
            }

            return ApiResponse.success(res, 'Mensaje eliminado correctamente');
        } catch (error) {
            return ApiResponse.error(res, error);
        }
    }
}
