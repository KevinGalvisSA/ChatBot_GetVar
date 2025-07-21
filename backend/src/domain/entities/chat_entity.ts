// backend/src/domain/entities/chat_entity.ts

import {
    Entity,
    PrimaryGeneratedColumn,
    Column,
    CreateDateColumn,
    UpdateDateColumn,
    OneToOne,
    JoinColumn,
    OneToMany
} from 'typeorm';
import { Customer } from './customer_entity';
import { Message } from './message_entity';

@Entity('chats')
export class Chat {
    @PrimaryGeneratedColumn()
    id!: number;

    @Column()
    customerId!: number;

    @OneToOne(() => Customer)
    @JoinColumn({ name: 'customerId' })
    customer!: Customer;

    // Dentro de la clase Chat
    @OneToMany(() => Message, (message) => message.chat)
    messages!: Message[];

    @Column({ type: 'datetime' })  // ← NOT NULL en DB
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
