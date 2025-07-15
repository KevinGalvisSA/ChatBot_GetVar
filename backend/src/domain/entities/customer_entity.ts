// src/domain/entities/customer_entity.ts

import {
    Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, UpdateDateColumn
} from 'typeorm';

@Entity('customers')
export class Customer {
    @PrimaryGeneratedColumn()
    id!: number;

    @Column({ type: 'varchar', length: 255 })
    name!: string;

    @Column({ type: 'bigint' })
    phone!: number;

    @Column({ type: 'int', nullable: true })
    createdBy!: number;

    @Column({ type: 'int', nullable: true })
    updatedBy!: number;

    @CreateDateColumn()
    createdAt!: Date;

    @UpdateDateColumn()
    updatedAt!: Date;
}
