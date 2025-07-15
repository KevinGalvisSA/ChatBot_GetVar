// src/adapters/http/controllers/chat_controller.ts

import { Request, Response } from 'express';
import { ChatService } from '../../../application/services/chat_service';

const service = new ChatService();

export const registerChatInfo = async (req: Request, res: Response) => {
    const chat = await service.createChat(req.body);
    return res.status(201).json(chat);
};

export const getChatInfoByCustomerId = async (req: Request, res: Response) => {
    const chats = await service.getChatsByCustomer(Number(req.params.customerId));
    return res.json(chats);
};

export const getChatsInfo = async (_: Request, res: Response) => {
    const chats = await service.getAllChats();
    return res.json(chats);
};

export const updateChatInfo = async (req: Request, res: Response) => {
    const updated = await service.updateChat(Number(req.params.id), req.body);
    return res.json(updated);
};

export const deleteChatInfo = async (req: Request, res: Response) => {
    const deleted = await service.deleteChat(Number(req.params.id));
    return res.json(deleted);
};
