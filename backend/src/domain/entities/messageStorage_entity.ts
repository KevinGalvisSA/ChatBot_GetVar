// src/domain/entities/message_storage_entity.ts

import {
    Entity, PrimaryGeneratedColumn, Column
} from 'typeorm';

@Entity('messageStorages')
export class MessageStorage {
    @PrimaryGeneratedColumn()
    id!: number;

    @Column({ type: 'bigint' })
    sessionId!: number;

    @Column({ type: 'text' })
    message!: string;

    @Column()
    customerId!: number;
}
