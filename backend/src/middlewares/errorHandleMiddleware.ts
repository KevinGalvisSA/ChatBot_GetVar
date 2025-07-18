import logger from '../handleUtils/logger';
import { Request, Response, NextFunction } from 'express';

async function errorManage(error: Error & { statusCode?: number }, req: Request, res: Response, _next: NextFunction) {
    // Si el error tiene un statusCode, lo usamos. Si no, usamos 500.
    const statusCode = error.statusCode || 500;

    // Log de Winston para registrar detalles del error
    logger.error({
        message: error.message,
        stack: error.stack,
        method: req.method,
        url: req.originalUrl,
        params: req.params,
        query: req.query,
        body: req.body,
        statusCode
    });

    // Enviar respuesta al cliente
    res.status(statusCode).json({
        message: 'Ocurrió un error interno',
        ...(process.env.NODE_ENV === 'development' ? { errorDetails: error.stack } : {}),
    });
}

export default errorManage;
