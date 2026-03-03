/**
 * Átomo: Button
 * Componente dinâmico para ações na interface.
 */
import React from 'react';

export default function Button({ children, onClick, type = 'button', disabled = false, variant = 'primary' }) {
  // Estilos inline simples para não dependermos de CSS global (em um app real usaríamos Tailwind ou Styled Components)
  const baseStyle = {
    padding: '0.5rem 1rem',
    borderRadius: '4px',
    border: 'none',
    cursor: disabled ? 'not-allowed' : 'pointer',
    fontWeight: 'bold',
    backgroundColor: variant === 'primary' ? '#007bff' : '#6c757d',
    color: '#fff',
    opacity: disabled ? 0.7 : 1,
  };

  return (
    <button 
      type={type} 
      onClick={onClick} 
      disabled={disabled} 
      style={baseStyle}
    >
      {children}
    </button>
  );
}