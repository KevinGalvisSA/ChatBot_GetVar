// backend/src/domain/entities/summary.entity.ts
import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn } from 'typeorm';

@Entity('summaries')
export class Summary {
    @PrimaryGeneratedColumn('uuid')
    id!: string;

    @Column({ type: 'uuid' })
    userId!: string;

    @Column({ type: 'text' })
    content!: string;

    @CreateDateColumn()
    createdAt!: Date;
}
