/**
 * Organismo: GeneratorForm
 * Formulário para capturar o tópico e o tipo de conteúdo desejado.
 */
import React, { useState } from 'react';
import Input from '../atoms/Input';
import Select from '../atoms/Select';
import Button from '../atoms/Button';

export default function GeneratorForm({ student, onSubmit, isLoading }) {
  const [topic, setTopic] = useState('');
  const [contentType, setContentType] = useState('');

  const contentOptions = [
    { value: 'conceitual', label: 'Explicação Conceitual' },
    { value: 'pratico', label: 'Exemplos Práticos' },
    { value: 'reflexao', label: 'Perguntas de Reflexão' },
    { value: 'visual', label: 'Resumo Visual/ASCII' }
  ];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!topic || !contentType) {
      alert("Preencha todos os campos!");
      return;
    }
    // Repassa os dados para o componente pai (App.jsx) lidar com a API
    onSubmit({ student_name: student.name, topic, content_type: contentType });
  };

  return (
    <form onSubmit={handleSubmit} style={{ border: '1px solid #ddd', padding: '1.5rem', borderRadius: '8px', marginTop: '1rem' }}>
      <h3>Gerar conteúdo para: <span style={{ color: '#007bff' }}>{student.name}</span></h3>
      
      <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '0.5rem' }}>Tópico da Aula:</label>
      <Input 
        value={topic} 
        onChange={(e) => setTopic(e.target.value)} 
        placeholder="Ex: Revolução Francesa, Álgebra Vetorial..." 
      />

      <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '0.5rem' }}>Tipo de Material:</label>
      <Select 
        value={contentType} 
        onChange={(e) => setContentType(e.target.value)} 
        options={contentOptions} 
      />

      <Button type="submit" variant="primary" disabled={isLoading}>
        {isLoading ? 'Gerando com IA...' : 'Gerar Conteúdo'}
      </Button>
    </form>
  );
}