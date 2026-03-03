import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
// Importação do index.css removida para garantir isolamento de estilos (Atomic Design)
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)