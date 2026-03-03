/**
 * Módulo de Serviço API (Axios).
 * Ponto central de comunicação HTTP com o backend (Flask).
 * * Preparado para Produção (Deploy):
 * Utiliza variáveis de ambiente (VITE_API_URL) para apontar para o servidor correto
 * na nuvem (ex: Render) ou usa o localhost:5000 como fallback durante o desenvolvimento.
 */
import axios from 'axios';

// Captura a URL da API configurada na plataforma de Deploy (Vercel) ou assume o ambiente local
const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

export const api = axios.create({
  baseURL: baseURL,
  
  // O tempo limite (timeout) foi aumentado para 15 segundos porque requisições
  // que dependem de LLMs (Gemini) e mecanismos de retentativa podem demorar mais.
  timeout: 15000, 
  
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json', // Boa prática: explicita ao servidor que esperamos JSON de volta
  },
});

/**
 * Interceptor Global de Respostas.
 * Atua como um "middleware" no frontend. Se houver um erro de rede grave (como o Render 
 * estar dormindo ou o CORS falhar), ele centraliza o log para facilitar o debug.
 */
api.interceptors.response.use(
  (response) => {
    // Se a requisição deu certo, apenas repassa os dados para o App.jsx
    return response;
  },
  (error) => {
    // Registra o erro de forma estruturada no console do navegador do usuário
    console.error(`[API Error] Falha de comunicação com ${baseURL}:`, error.message);
    
    // Rejeita a promessa para que o bloco "catch" do App.jsx lide com a UI (mensagens na tela)
    return Promise.reject(error);
  }
);