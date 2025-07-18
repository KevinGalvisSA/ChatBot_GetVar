import express from 'express';
import http from 'http';
import { Server } from 'socket.io';
import messageRoutes from './adapters/http/routes/message_routes';
import 'reflect-metadata';
import { AppDataSource } from './config/data_source';
import errorManage from './middlewares/errorHandleMiddleware';
import morgan from 'morgan';
import logger from './handleUtils/logger';  // Importa el logger

const app = express();
app.use(express.json());

// Configurar morgan para logging de solicitudes HTTP
const stream = {
  write: (message: string) => logger.info(message.trim()),  // Utiliza logger.info
};

app.use(morgan('combined', { stream }));

// Usar las rutas de mensajes
app.use('/api', messageRoutes);

// Ruta para probar errores (solo para pruebas)
app.get('/error-test', (req, res) => {
  throw new Error('Error de prueba');
});

// Usar el middleware de manejo de errores después de todas las rutas
app.use(errorManage);  // Esto captura cualquier error no manejado previamente

// Crear el servidor HTTP para WebSocket
const server = http.createServer(app);

// Crear la instancia del servidor Socket.IO
const io = new Server(server, {
  cors: {
    origin: "*",  // Permite que cualquier origen se conecte
    methods: ["GET", "POST"],
    credentials: true,
  }
});

io.on('connection', (socket) => {
  console.log('Cliente conectado:', socket.id);

  // Escuchar mensajes de clientes (enviados desde frontend)
  socket.on('send_message', async (data) => {
    try {
      console.log('Mensaje recibido desde el frontend:', data);

      // Enviar el mensaje al servicio Python (FastAPI)
      const pythonResponse = await sendMessageToPython(data.message);

      // Emitir la respuesta del servicio Python al frontend (al cliente conectado)
      socket.emit('receive_message', pythonResponse);
    } catch (error) {
      // Manejo del error si la llamada a FastAPI falla
      socket.emit('receive_message', '❌ Error al procesar el mensaje');
      throw error;  // Lanza el error para que lo capture el middleware global
    }
  });

  socket.on('disconnect', () => {
    console.log('Cliente desconectado:', socket.id);
  });
});

// Función para enviar mensaje al servicio Python
async function sendMessageToPython(message: string) {
  console.log('Enviando mensaje a FastAPI:', message);  // Log antes de enviar el mensaje

  try {
    const response = await fetch('http://localhost:8000/chat', {  // URL del servicio FastAPI
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message })
    });

    if (!response.ok) {
      throw new Error('Error en la respuesta de FastAPI');
    }

    const data = await response.json();
    console.log('Respuesta recibida de FastAPI:', data);  // Log después de recibir la respuesta
    return data.response;  // Retorna la respuesta de la IA o el error
  } catch (error) {
    console.error('Error al llamar a FastAPI:', error);  // Log para cualquier error de la llamada fetch
    throw error;  // Lanzamos el error para que sea capturado por el middleware global
  }
}

const PORT = process.env.PORT || 4000;

// Inicializa la base de datos y el servidor
AppDataSource.initialize()
  .then(() => {
    server.listen(PORT, () => {
      console.log(`🚀 Servidor backend escuchando en http://localhost:${PORT}`);
    });
  })
  .catch((err) => {
    console.error("❌ Error al iniciar la base de datos:", err);
  });
