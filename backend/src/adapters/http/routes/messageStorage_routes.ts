// backend/src/adapters/http/routes/message_storage_routes.ts

import { Router } from 'express';
import { MessageStorageController } from '../controllers/messageStorage_controller';

const router = Router();


router.post('/', MessageStorageController.create); // Crear un mensaje en storage
router.get('/customer/:id_customer', MessageStorageController.getByid_customer); // Obtener mensaje por ID de cliente
router.get('/session/:session_id', MessageStorageController.getBysession_id); // Obtener mensaje por ID de sesión
router.delete('/customer/:id_customer', MessageStorageController.deleteByid_customer); // Eliminar mensaje por ID de cliente

export default router;
