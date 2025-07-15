// src/adapters/http/routes/chat_routes.ts

import { Router } from 'express';
import {
    registerChatInfo,
    getChatInfoByCustomerId,
    getChatsInfo,
    updateChatInfo,
    deleteChatInfo
} from '../controllers/chat_controller';

const router = Router();

router.post('/', registerChatInfo);
router.get('/', getChatsInfo);
router.get('/customer/:customerId', getChatInfoByCustomerId);
router.put('/:id', updateChatInfo);
router.delete('/:id', deleteChatInfo);

export default router;
