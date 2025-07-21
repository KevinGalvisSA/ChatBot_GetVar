// backend/src/domain/entities/message_storage_entity.ts

import {
  Entity,
  PrimaryGeneratedColumn,
  Column,
  CreateDateColumn,
  OneToOne,
  JoinColumn,
} from 'typeorm';
import { Customer } from './customer_entity';

@Entity('message_storage')
export class MessageStorage {
  @PrimaryGeneratedColumn()
  id!: number;

  @Column({ name: 'id_customer' })
  customerId!: number;

  @OneToOne(() => Customer)
  @JoinColumn({ name: 'id_customer' })  // clave foránea explícita
  customer!: Customer;

  @Column({ name: 'session_id', type: 'bigint' })
  sessionId!: number;

  @Column({ type: 'text' })
  message!: string;

  @Column({ name: 'message_type', type: 'varchar', length: 50 })
  messageType!: string;

  @CreateDateColumn({ name: 'created_at', type: 'timestamp' })
  createdAt!: Date;
}
