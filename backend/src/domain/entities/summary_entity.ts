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
    session_id!: number;

    @Column({ type: 'mediumint', unsigned: true })
    chat_id!: number;

    @ManyToOne(() => Chat)
    @JoinColumn({ name: 'chat_id' })
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
