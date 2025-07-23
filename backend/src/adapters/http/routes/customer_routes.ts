// backend/src/adapters/http/routes/customer_routes.ts

import { Router } from 'express';
import { CustomerController } from '../controllers/customer_controller';

const router = Router();

router.post('/', CustomerController.getOrCreate); // Crea o retorna si ya existe
router.get('/:id', CustomerController.getById); // Obtener por ID
router.get('/phone/:phone', CustomerController.getByphone); // Obtener por número de teléfono
router.put('/:id', CustomerController.update); // Actualizar cliente
router.delete('/:id', CustomerController.delete); // Eliminar cliente

export default router;
