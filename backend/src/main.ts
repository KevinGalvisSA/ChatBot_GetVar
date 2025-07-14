// backend/src/main.ts
/*
import express from 'express';
import messageRoutes from './adapters/http/routes/message_routes';
import 'reflect-metadata';
import { AppDataSource } from './config/data-source';

const app = express();
app.use(express.json());

app.use('/api', messageRoutes);

const PORT = process.env.PORT || 4000;

AppDataSource.initialize()
  .then(() => {
    app.listen(PORT, () => {
      console.log(`🚀 Servidor backend escuchando en http://localhost:${PORT}`);
    });
  })
  .catch((err) => {
    console.error("❌ Error al iniciar la base de datos:", err);
  });
*/