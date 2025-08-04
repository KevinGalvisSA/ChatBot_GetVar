import { Router } from 'express';
import { WebhookController } from '../controllers/webhook_controller';

const router = Router();

router.get('/whatsapp', WebhookController.verifyWhatsAppWebhook);
router.post('/whatsapp', WebhookController.handleWhatsAppWebhook);
router.get('/storage/:phone', WebhookController.getMessageStorage);

export default router;
