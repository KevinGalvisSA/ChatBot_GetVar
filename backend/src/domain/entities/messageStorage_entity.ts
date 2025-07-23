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

@Entity('messageStorage')
export class MessageStorage {
  @PrimaryGeneratedColumn()
  id!: number;

  @Column({ name: 'id_customer' })
  id_customer!: number;

  @OneToOne(() => Customer)
  @JoinColumn({ name: 'id_customer' })  // clave foránea explícita
  customer!: Customer;

  @Column({ name: 'id_session', type: 'bigint' })
  session_id!: number;

  @Column({ type: 'text' })
  message!: string;

  @Column({ name: 'message_type', type: 'varchar', length: 50 })
  message_type!: string;
}
