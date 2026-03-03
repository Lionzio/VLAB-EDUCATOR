/**
 * Átomo: Select
 * Caixa de seleção dinâmica baseada em um array de opções.
 */
import React from 'react';

export default function Select({ value, onChange, options, required = false }) {
  const baseStyle = {
    padding: '0.5rem',
    borderRadius: '4px',
    border: '1px solid #ccc',
    width: '100%',
    boxSizing: 'border-box',
    marginBottom: '1rem'
  };

  return (
    <select value={value} onChange={onChange} required={required} style={baseStyle}>
      <option value="" disabled>Selecione uma opção...</option>
      {/* Renderização Iterativa (DRY) das opções */}
      {options.map((opt) => (
        <option key={opt.value} value={opt.value}>
          {opt.label}
        </option>
      ))}
    </select>
  );
}