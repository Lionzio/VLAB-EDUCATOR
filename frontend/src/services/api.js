/**
 * Configuração centralizada do cliente HTTP (Axios).
 * Aponta para o nosso backend Flask.
 */
import axios from 'axios';

export const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  timeout: 10000, // 10 segundos de limite
  headers: {
    'Content-Type': 'application/json',
  },
});