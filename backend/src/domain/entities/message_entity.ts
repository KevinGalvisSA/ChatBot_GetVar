// backend/src/domain/entities/message_entity.ts

import {
    Entity,
    PrimaryGeneratedColumn,
    Column,
    CreateDateColumn,
    UpdateDateColumn,
    Check,
    ManyToOne,
    JoinColumn
} from 'typeorm';
import { Chat } from './chat_entity';

@Check(`"type" IN (0, 1)`)
@Entity('messages')
export class Message {
    @PrimaryGeneratedColumn()
    id!: number;

    @Column({ type: 'tinyint' })
    type!: number; // 0 = user, 1 = bot

    @Column({ type: 'text' })
    content!: string;

    @Column({ name: 'chat_id' })
    chat_id!: number;

    // Relación Many-to-One con Chat
    @ManyToOne(() => Chat, (chat: Chat) => chat.messages, { onDelete: 'CASCADE' })
    @JoinColumn({ name: 'chat_id' })
    chat!: Chat;


    @Column({ type: 'int', nullable: true })
    createdBy!: number;

    @Column({ type: 'int', nullable: true })
    updatedBy!: number;

    @CreateDateColumn()
    createdAt!: Date;

    @UpdateDateColumn()
    updatedAt!: Date;
}
