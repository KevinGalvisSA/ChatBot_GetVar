// backend/src/adapters/http/routes/message_storage_routes.ts

import { Router } from 'express';
import { MessageStorageController } from '../controllers/messageStorage_controller';

const router = Router();


router.post('/', MessageStorageController.create); // Crear un mensaje en storage
router.get('/customer/:customerId', MessageStorageController.getByCustomerId); // Obtener mensaje por ID de cliente
router.get('/session/:sessionId', MessageStorageController.getBySessionId); // Obtener mensaje por ID de sesión
router.delete('/customer/:customerId', MessageStorageController.deleteByCustomerId); // Eliminar mensaje por ID de cliente

export default router;
