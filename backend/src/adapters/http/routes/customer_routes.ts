// src/adapters/http/routes/customer_routes.ts

import { Router } from 'express';
import {
  createCustomer,
  getCustomer,
  getAllCustomers,
  updateCustomer,
  deleteCustomer
} from '../controllers/customer_controller';

const router = Router();

router.post('/', createCustomer);
router.get('/', getAllCustomers);
router.get('/:id', getCustomer);
router.put('/:id', updateCustomer);
router.delete('/:id', deleteCustomer);

export default router;
