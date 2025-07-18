// logger.ts
import winston from 'winston';

// Definir el tipo de Logger
const logger: winston.Logger = winston.createLogger({
  level: 'error',  // Solo se registrarán errores
  format: winston.format.combine(
    winston.format.timestamp(),  // Agrega la marca de tiempo
    winston.format.json()         // Formato JSON
  ),
  transports: [
    new winston.transports.Console(),  // Muestra los logs en la consola
    new winston.transports.File({ filename: 'logs/errors.log' })  // Guarda los logs en un archivo
  ]
});

export default logger;
