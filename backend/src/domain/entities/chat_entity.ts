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

@Entity('chat')
export class Chat {
    @PrimaryGeneratedColumn()
    id!: number;

    @Column()
    id_customer!: number;

    @OneToOne(() => Customer)
    @JoinColumn({ name: 'id_customer' })
    customer!: Customer;

    @OneToMany(() => Message, (message) => message.chat)
    messages!: Message[];

    @Column({ type: 'datetime' })
    last_connection!: Date;

    @Column({ type: 'int', nullable: true })
    createdBy!: number;

    @Column({ type: 'int', nullable: true })
    updatedBy!: number;

    @Column({ type: 'tinyint' })
    state!: number;

    @CreateDateColumn({ type: 'timestamp' })
    createdAt!: Date;

    @UpdateDateColumn({ type: 'timestamp' })
    updatedAt!: Date;
}
