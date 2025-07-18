// backend/src/domain/entities/chat_entity.ts

import {
    Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, UpdateDateColumn, OneToOne, JoinColumn
} from 'typeorm';
import { Customer } from './customer_entity';

@Entity('chats')
export class Chat {
    @PrimaryGeneratedColumn()
    id!: number;

    @Column()
    customerId!: number; // Relacion con el ID del Customer

    @OneToOne(() => Customer)  // Relación uno a uno con Customer
    @JoinColumn({ name: 'customerId' })  // El chat "pertenece" a un solo customer
    customer!: Customer;

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