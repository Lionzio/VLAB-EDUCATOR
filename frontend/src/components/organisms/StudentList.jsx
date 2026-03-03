/**
 * Organismo: StudentList
 * Renderiza iterativamente uma lista de moléculas StudentListItem baseada nos dados fornecidos.
 */
import React from 'react';
import StudentListItem from '../molecules/StudentListItem';

export default function StudentList({ students, onStudentSelect }) {
  if (!students || students.length === 0) {
    return <p>Nenhum aluno carregado no momento.</p>;
  }

  return (
    <div>
      <h2>Alunos Cadastrados</h2>
      {/* Renderização Iterativa - Apenas 1 componente base sendo repetido pelo motor do React */}
      {students.map((student) => (
        <StudentListItem 
          key={student.id} 
          student={student} 
          onSelect={onStudentSelect} 
        />
      ))}
    </div>
  );
}