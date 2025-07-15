// src/adapters/http/controllers/messageStorage_controller.ts

import { Request, Response } from 'express';
import { MessageStorageService } from '../../../application/services/messageStorage_service';

const service = new MessageStorageService();

export const createMessageStorageData = async (req: Request, res: Response) => {
    const result = await service.createMessageStorage(req.body);
    return res.status(201).json(result);
};

export const getStorageDataByCustomer = async (req: Request, res: Response) => {
    const storages = await service.getStorageByCustomer(Number(req.params.customerId));
    return res.json(storages);
};

export const getAllStoragesData = async (_: Request, res: Response) => {
    const storages = await service.getAllStorages();
    return res.json(storages);
};

export const updateStorageData = async (req: Request, res: Response) => {
    const updated = await service.updateStorage(Number(req.params.id), req.body);
    return res.json(updated);
};

export const deleteStorageData = async (req: Request, res: Response) => {
    const deleted = await service.deleteStorage(Number(req.params.id));
    return res.json(deleted);
};
