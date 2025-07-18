import winston from 'winston';

// Definir el tipo de Logger
const logger: winston.Logger = winston.createLogger({
  level: 'error',  // Solo se registrarán errores
  format: winston.format.combine(
    winston.format.timestamp(),  // Agrega la marca de tiempo
    winston.format.printf((info) => {
      // Usamos JSON.stringify con espaciado de 2 espacios para los logs
      return JSON.stringify(info, null); // Agregar indentación
    })
  ),
  transports: [
    new winston.transports.Console(),  // Muestra los logs en la consola
    new winston.transports.File({ filename: 'logs/errors.log' })  // Guarda los logs en un archivo
  ]
});

export default logger;
