// src/domain/entities/chat_entity.ts

import {
    Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, UpdateDateColumn
} from 'typeorm';

@Entity('chats')
export class Chat {
    @PrimaryGeneratedColumn()
    id!: number;

    @Column()
    customerId!: number;

    @Column({ type: 'datetime', nullable: true })
    lastConnection!: Date;

    @Column({ type: 'int', nullable: true })
    createdBy!: number;

    @Column({ type: 'int', nullable: true })
    updatedBy!: number;

    @CreateDateColumn()
    createdAt!: Date;

    @UpdateDateColumn()
    updatedAt!: Date;
}
