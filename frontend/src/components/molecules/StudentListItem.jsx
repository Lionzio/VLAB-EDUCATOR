/**
 * Molécula: StudentListItem
 * Representa a exibição de um único aluno. Altamente agnóstico e sem dados hardcoded.
 */
import React from 'react';
import Button from '../atoms/Button';

export default function StudentListItem({ student, onSelect }) {
  const cardStyle = {
    border: '1px solid #ccc',
    padding: '1rem',
    margin: '0.5rem 0',
    borderRadius: '8px',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#f8f9fa'
  };

  return (
    <div style={cardStyle}>
      <div>
        <h3 style={{ margin: '0 0 0.5rem 0' }}>{student.name}</h3>
        <p style={{ margin: 0, fontSize: '0.9rem', color: '#555' }}>
          Idade: {student.age} | Nível: {student.level} | Estilo: {student.learning_style}
        </p>
      </div>
      
      {/* Reutilizando nosso Átomo */}
      <Button onClick={() => onSelect(student)} variant="primary">
        Selecionar
      </Button>
    </div>
  );
}