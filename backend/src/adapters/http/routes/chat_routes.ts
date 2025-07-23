// backend/src/adapters/http/routes/chat_routes.ts

import { Router } from 'express';
import { ChatController } from '../controllers/chat_controller';

const router = Router();

router.post('/', ChatController.createIfNotExists); // Crear o retornar el chat existente
router.get('/', ChatController.list); // Obtener todos los chats
router.get('/:id', ChatController.getById); // Obtener chat por ID
router.get('/customer/:id_customer', ChatController.getByid_customer); // Obtener chat por ID del cliente
router.put('/:id', ChatController.update); // Actualizar chat
router.patch('/:id/state', ChatController.updateState); // Cambiar el estado del chat y generar resumen si es inactivo
router.delete('/:id', ChatController.delete); // Eliminar chat

export default router;
