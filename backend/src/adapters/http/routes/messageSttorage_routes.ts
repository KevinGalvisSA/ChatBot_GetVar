// backend/src/adapters/http/routes/messageStorage_routes.ts

import { Router } from 'express';
import { MessageStorageController } from '../controllers/messageStorage_controller';

const router = Router();

router.post('/', MessageStorageController.create);
router.get('/customer/:customerId', MessageStorageController.getByCustomerId);
router.get('/session/:sessionId', MessageStorageController.getBySessionId);
router.delete('/customer/:customerId', MessageStorageController.deleteByCustomerId);

export default router;
