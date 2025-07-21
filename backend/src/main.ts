import express from 'express';
import http from 'http';
import { Server } from 'socket.io';
import messageRoutes from './adapters/http/routes/message_routes';
import 'reflect-metadata';
import { AppDataSource } from './config/data_source';
import errorManage from './middlewares/errorHandleMiddleware';
import morgan from 'morgan';
import logger from './handleUtils/logger';
import { configureSocket } from './config/socket';

const app = express();
app.use(express.json());

const stream = {
  write: (message: string) => logger.info(message.trim()),
};

app.use(morgan('combined', { stream }));
app.use('/api', messageRoutes);

app.get('/error-test', (req, res) => {
  throw new Error('Error de prueba');
});

app.use(errorManage);

const server = http.createServer(app);

const io = new Server(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"],
    credentials: true,
  },
});

configureSocket(io);  // Aquí se delega la lógica del WebSocket

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
