import { Chat } from '../../domain/entities/chat_entity';
import { ChatRepository } from '../../infrastructure/repositories/chat_repository';
import { SummaryRepository } from '../../infrastructure/repositories/summary_repository';
import { CustomerRepository } from '../../infrastructure/repositories/customer_repository'; 
import { pythonCommunication } from './pythonCommunication';

export class ChatService {
    private chatRepository: ChatRepository;
    private resumenRepository: SummaryRepository;
    private customerRepository: CustomerRepository;

    constructor() {
        this.chatRepository = new ChatRepository();
        this.resumenRepository = new SummaryRepository();
        this.customerRepository = new CustomerRepository(); 
    }

    async createChatIfNotExists(id_customer: number): Promise<Chat> {
        const existing = await this.chatRepository.findByid_customer(id_customer);
        if (existing) return existing;

        const chat = await this.chatRepository.create({
            id_customer,
            last_connection: new Date(),
            createdBy: id_customer,
            updatedBy: id_customer,
        });

        return chat;
    }

    async getChatById(id: number): Promise<Chat> {
        const chat = await this.chatRepository.findById(id);
        if (!chat) throw new Error('Chat no encontrado');
        return chat;
    }

    async getChatByid_customer(id_customer: number): Promise<Chat> {
        const chat = await this.chatRepository.findByid_customer(id_customer);
        if (!chat) throw new Error('El cliente no tiene un chat asociado');
        return chat;
    }

    async updateChat(id: number, updates: Partial<Chat>): Promise<Chat> {
        return await this.chatRepository.update(id, updates);
    }

    async deleteChat(id: number): Promise<void> {
        await this.chatRepository.delete(id);
    }

    async listChats(): Promise<Chat[]> {
        return await this.chatRepository.findAll();
    }

    async updateChatStateByCustomer(id_customer: number, newState: number): Promise<Chat> {
        const chat = await this.chatRepository.findByid_customer(id_customer);
        if (!chat) throw new Error('Chat no encontrado para este cliente');

        if (chat.state === newState) return chat;

        const updatedChat = await this.chatRepository.updateState(chat.id, newState);

        if (newState === 0) {
            try {
                const customer = await this.customerRepository.findById(id_customer); 
                if (!customer) throw new Error('Cliente no encontrado');

                const id_session = customer.phone_number.toString(); 

                const resumen = await pythonCommunication.generateSummary(chat.id, id_session);

                await this.resumenRepository.create({
                    id_session: customer.phone_number,
                    chatId: chat.id,
                    message: resumen,
                    createdAt: new Date(),
                    updatedAt: new Date(),
                });

                console.log('✅ Resumen guardado en base de datos');
            } catch (error) {
                console.error('❌ Error al generar o guardar resumen:', error);
            }
        }

        return updatedChat;
    }

    async getResumesByChat(chatId: number) {
        return await this.resumenRepository.findByChatId(chatId);
    }
}
