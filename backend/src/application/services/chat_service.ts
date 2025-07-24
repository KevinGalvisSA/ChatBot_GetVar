import { Chat } from '../../domain/entities/chat_entity';
import { ChatRepository } from '../../infrastructure/repositories/chat_repository';
import { SummaryRepository } from '../../infrastructure/repositories/summary_repository';
import { CustomerRepository } from '../../infrastructure/repositories/customer_repository';
import { pythonCommunication } from './pythonCommunication';
import { MessageService } from './message_service';

export class ChatService {
    private messageService: MessageService;
    private chatRepository: ChatRepository;
    private resumenRepository: SummaryRepository;
    private customerRepository: CustomerRepository;

    constructor() {
        this.messageService = new MessageService();
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

    async getChatsInactiveForMinutes(minutes: number): Promise<Chat[]> {
        const threshold = new Date(Date.now() - minutes * 60 * 1000);
        return await this.chatRepository.getInactiveSince(threshold);
    }

    async handleUserMessageAndResponse(
        id_customer: number,
        userMessage: string,
        messageService: MessageService
    ): Promise<string> {
        const customer = await this.customerRepository.findById(id_customer);
        if (!customer) throw new Error('Cliente no encontrado');

        const chat = await this.createChatIfNotExists(id_customer);
        const session_id = customer.phone.toString();

        // Guardar mensaje del usuario
        await this.messageService.createMessage({
            content: userMessage,
            type: 0,
            chat,
            createdAt: new Date(),
            updatedAt: new Date(),
        });

        // Obtener respuesta del bot
        const botResponse = await pythonCommunication.sendMessageToPython(userMessage, session_id);

        // Guardar respuesta del bot
        await messageService.createMessage({
            content: botResponse,
            type: 1,
            chat,
            createdAt: new Date(),
            updatedAt: new Date(),
        });

        return botResponse;
    }


    async updateChatStateByCustomer(id_customer: number, newState: number): Promise<Chat> {
        console.log('🔍 updateChatStateByCustomer llamado con:', id_customer, newState);

        const chat = await this.chatRepository.findByid_customer(id_customer);
        if (!chat) throw new Error('Chat no encontrado para este cliente');

        console.log('Datos del chat:', chat);

        let updatedChat: Chat;

        if (chat.state !== newState) {
            updatedChat = await this.chatRepository.updateState(chat.id, newState);
            console.log('✅ Estado del chat actualizado:', updatedChat);
        } else {
            updatedChat = chat;
            console.log('ℹ️ Estado del chat ya era el solicitado, no se actualizó.');
        }

        if (newState === 0) {
            try {
                const customer = await this.customerRepository.findById(id_customer);
                if (!customer) throw new Error('Cliente no encontrado');

                const session_id = customer.phone.toString();

                const resumen = await pythonCommunication.generateSummary(chat.id, session_id);
                console.log('🧠 Resumen generado:', resumen);

                await this.resumenRepository.create({
                    session_id: customer.phone,
                    chat_id: chat.id,
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

    async getResumesByChat(chat_id: number) {
        return await this.resumenRepository.findBychat_id(chat_id);
    }
}
