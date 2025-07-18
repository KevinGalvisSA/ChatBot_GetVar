import express from 'express';
import http from 'http';
import { Server } from 'socket.io';  // Importar correctamente Server de socket.io
import messageRoutes from './adapters/http/routes/message_routes';
import 'reflect-metadata';
import { AppDataSource } from './config/data_source';
import errorManage from './middlewares/errorHandleMiddleware'

const app = express();
app.use(express.json());

app.use('/api', messageRoutes);
app.use(errorManage)

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
    console.log('Mensaje recibido desde el frontend:', data);

    // Enviar el mensaje al servicio Python (FastAPI)
    const pythonResponse = await sendMessageToPython(data.message);

    // Log para verificar la respuesta de Gemini
    console.log('Respuesta recibida desde Gemini:', pythonResponse);

    // Emitir la respuesta del servicio Python al frontend (al cliente conectado)
    socket.emit('receive_message', pythonResponse);
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
      console.error('Error en la respuesta de FastAPI:', response.statusText);
    }

    const data = await response.json();
    console.log('Respuesta recibida de FastAPI:', data);  // Log después de recibir la respuesta
    return data.response;  // Retorna la respuesta de la IA o el error
  } catch (error) {
    console.error('Error al llamar a FastAPI:', error);  // Log para cualquier error de la llamada fetch
    return '❌ Error al comunicar con FastAPI';
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

  // Iniciar main.ts
  // npm run main