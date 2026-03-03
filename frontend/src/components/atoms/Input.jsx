/**
 * Átomo: Input
 * Campo de texto genérico e controlado.
 */
import React from 'react';

export default function Input({ type = 'text', value, onChange, placeholder, required = false }) {
  const baseStyle = {
    padding: '0.5rem',
    borderRadius: '4px',
    border: '1px solid #ccc',
    width: '100%',
    boxSizing: 'border-box',
    marginBottom: '1rem'
  };

  return (
    <input
      type={type}
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      required={required}
      style={baseStyle}
    />
  );
}