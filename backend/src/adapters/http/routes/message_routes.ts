// src/adapters/http/routes/message_routes.ts

import { Router } from 'express';
import {
    createMessageData,
    getMessagesDataByChat,
    getAllMessagesData,
    updateMessageData,
    deleteMessageData
} from '../controllers/message_controller';

const router = Router();

router.post('/', createMessageData);
router.get('/', getAllMessagesData);
router.get('/chat/:chatId', getMessagesDataByChat); 
router.put('/:id', updateMessageData);
router.delete('/:id', deleteMessageData);

export default router;
