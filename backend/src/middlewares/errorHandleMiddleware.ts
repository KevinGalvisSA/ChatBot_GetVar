// Middleware manejo de errores
import logger from '../handleUtils/logger';

async function errorManage(error: Error, req: any, res: any, next: any) {
    logger.error('Algo salió mal', { 
        message: error.message,
        stack: error.stack 
    });

    res.status(500).json({ message: 'Ocurrió un error interno' });
}

export default errorManage;
