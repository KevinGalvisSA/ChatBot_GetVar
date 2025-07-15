// src/adapters/http/routes/messageStorage_routes.ts

import { Router } from 'express';
import {
    createMessageStorageData,
    getStorageDataByCustomer,
    getAllStoragesData,
    updateStorageData,
    deleteStorageData
} from '../controllers/messageStorage_controller';

const router = Router();

router.post('/', createMessageStorageData);
router.get('/', getAllStoragesData);
router.get('/customer/:customerId', getStorageDataByCustomer);
router.put('/:id', updateStorageData);
router.delete('/:id', deleteStorageData);

export default router;
