import express from 'express';
import http from 'http';
import { Server } from 'socket.io';
import 'reflect-metadata';
import { AppDataSource } from './config/data_source';
import { configureSocket } from './config/socket';
import errorManage from './middlewares/errorHandleMiddleware';
import morgan from 'morgan';
import logger from './handleUtils/logger';
import messageRoutes from './adapters/http/routes/message_routes';
import customerRoutes from './adapters/http/routes/customer_routes';
import chatRoutes from './adapters/http/routes/chat_routes';
import messageStorageRoutes from './adapters/http/routes/messageStorage_routes';
import webhookRoutes from './adapters/http/routes/webhook_routes';


const app = express();
app.use(express.json());

const stream = {
  write: (message: string) => logger.info(message.trim()),
};

app.use(morgan('combined', { stream }));

// Registro de rutas
app.use('/api/messages', messageRoutes);
app.use('/api/customers', customerRoutes);
app.use('/api/chats', chatRoutes);
app.use('/api/message-storage', messageStorageRoutes);
app.use('/webhook', webhookRoutes);

// Ruta de prueba para errores
app.get('/error-test', (req, res) => {
  throw new Error('Error de prueba');
});

// Middleware de manejo de errores
app.use(errorManage);

const server = http.createServer(app);

// Configuración de WebSocket
const io = new Server(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"],
    credentials: true,
  },
});

configureSocket(io);

const PORT = process.env.PORT || 4000;

AppDataSource.initialize()
  .then(() => {
    server.listen(PORT, () => {
      console.log(`🚀 Servidor backend escuchando en http://localhost:${PORT}`);
    });
  })
  .catch((err) => {
    console.error("❌ Error al iniciar la base de datos:", err);
  });
