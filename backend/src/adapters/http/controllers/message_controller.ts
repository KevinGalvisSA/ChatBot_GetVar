/*
import { Request, Response } from 'express';
import { MessageService } from '../../../application/services/message_service';
import { SummaryService } from '../../../application/services/summary_service';
import { answer_with_gemini } from '../../../infrastructure/gemini_integration';

const messageService = new MessageService();
const summaryService = new SummaryService();

const END_CONVERSATION_KEYWORDS = [
    "gracias", "muchas gracias", "eso era todo", "eso es todo", "me sirvió",
    "me ayudó", "muy útil", "hasta luego", "nos vemos", "listo", "ya terminé"
];

function isEndOfConversation(text: string): boolean {
    const normalized = text.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    return END_CONVERSATION_KEYWORDS.some(phrase => normalized.includes(phrase));
}

export const saveMessages = async (req: Request, res: Response) => {
    const { userId, message } = req.body;

    await messageService.saveUserMessage(userId, message);
    const botResponse = await req.langgraph.run(message);
    await messageService.saveBotMessage(userId, botResponse);

    if (isEndOfConversation(message)) {
        const history = await messageService.getConversation(userId);
        const transcript = history.map(msg => `${msg.role === 'user' ? 'Usuario' : 'Bot'}: ${msg.content}`).join('\n');

        const resumen = await answer_with_gemini(`Haz un resumen ejecutivo de esta conversación:\n${transcript}`);
        await summaryService.save(userId, resumen);

        console.log(`📝 Resumen generado:\n${resumen}`);
    }

    return res.json({ response: botResponse });
};

export const getMessages = async (req: Request, res: Response) => {
    const userId = req.params.userId;
    const messages = await messageService.getConversation(userId);
    return res.json(messages);
};

export const getLatestSummary = async (req: Request, res: Response) => {
    const userId = req.params.userId;
    const summary = await summaryService.getLatest(userId);
    return res.json(summary);
};
*/