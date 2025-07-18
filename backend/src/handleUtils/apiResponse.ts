// backend/src/handleUtils/apiResponse.ts
import { Response } from 'express';

export class ApiResponse {
    static success(res: Response, message: string, data: any = null, statusCode: number = 200) {
        return res.status(statusCode).json({ message, data });
    }

    static created(res: Response, message: string, data: any = null) {
        return res.status(201).json({ message, data });
    }

    static notFound(res: Response, message: string = "Recurso no encontrado") {
        return res.status(404).json({ error: message });
    }

    static badRequest(res: Response, message: string, data: any = null) {
        return res.status(400).json({ error: message, data });
    }

    static unauthorized(res: Response, message: string = "No autorizado") {
        return res.status(401).json({ error: message });
    }

    static forbidden(res: Response, message: string = "Acceso denegado") {
        return res.status(403).json({ error: message });
    }

    static internalServerError(res: Response, message: string = "Error interno del servidor") {
        return res.status(500).json({ error: message });
    }

    static error(res: Response, error: any, statusCode: number = 400) {
        if (typeof error === 'object' && error !== null && ('error' in error || 'data' in error)) {
            return res.status(statusCode).json({
                error: error.error ?? 'Error desconocido',
                data: error.data ?? undefined
            });
        }
        if (error instanceof Error) {
            return res.status(statusCode).json({ error: error.message });
        }
        return res.status(statusCode).json({ error });
    }
}
