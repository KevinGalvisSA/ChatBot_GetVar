// backend/src/domain/entities/resumen_entity.ts

import {
    Entity,
    PrimaryGeneratedColumn,
    Column,
    CreateDateColumn,
    UpdateDateColumn,
    ManyToOne,
    JoinColumn,
} from 'typeorm';
import { Chat } from './chat_entity';

@Entity('summary_storage')
export class Summary {
    @PrimaryGeneratedColumn()
    id!: number;

    @Column({ type: 'bigint' })
    id_session!: number;

    @Column({ type: 'mediumint', unsigned: true })
    chatId!: number;

    @ManyToOne(() => Chat)
    @JoinColumn({ name: 'chatId' })
    chat!: Chat;

    @Column({ type: 'text' })
    message!: string;

    @Column({ type: 'mediumint', unsigned: true, nullable: true })
    createdBy!: number;

    @Column({ type: 'mediumint', unsigned: true, nullable: true })
    updatedBy!: number;

    @CreateDateColumn()
    createdAt!: Date;

    @UpdateDateColumn()
    updatedAt!: Date;
}
