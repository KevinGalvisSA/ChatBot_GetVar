// src/adapters/http/controllers/message_controller.ts

import { Request, Response } from 'express';
import { MessageService } from '../../../application/services/message_service';

const service = new MessageService();

export const createMessageData = async (req: Request, res: Response) => {
    const msg = await service.createMessage(req.body);
    return res.status(201).json(msg);
};

export const getMessagesDataByChat = async (req: Request, res: Response) => {
    const messages = await service.getMessagesByChat(Number(req.params.chatId));
    return res.json(messages);
};

export const getAllMessagesData = async (_: Request, res: Response) => {
    const messages = await service.getAllMessages();
    return res.json(messages);
};

export const updateMessageData = async (req: Request, res: Response) => {
    const updated = await service.updateMessage(Number(req.params.id), req.body);
    return res.json(updated);
};

export const deleteMessageData = async (req: Request, res: Response) => {
    const deleted = await service.deleteMessage(Number(req.params.id));
    return res.json(deleted);
};
