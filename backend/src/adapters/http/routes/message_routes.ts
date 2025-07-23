// backend/src/adapters/http/routes/message_routes.ts

import { Router } from 'express';
import { MessageController } from '../controllers/message_controller';

const router = Router();

router.post('/', MessageController.create); // Crear un nuevo mensaje
router.get('/chat/:chat_id', MessageController.getBychat_id); // Obtener todos los mensajes de un chat
router.delete('/:id', MessageController.deleteById); // Eliminar un mensaje por su ID

export default router;
