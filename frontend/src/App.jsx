/**
 * Componente Raiz da Aplicação.
 * Orquestra o roteamento e as páginas (Nesta etapa, testaremos as chamadas HTTP).
 */
import React, { useState, useEffect } from 'react';
import { api } from './services/api';
import StudentList from './components/organisms/StudentList';

function App() {
  const [studentsData, setStudentsData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Chamada à API Flask logo que o React monta a tela
    api.get('/students')
      .then((response) => {
        setStudentsData(response.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setError('Falha ao conectar com o servidor Flask.');
        setLoading(false);
      });
  }, []);

  const handleSelectStudent = (student) => {
    alert(`Preparando ambiente para: ${student.name} (Funcionalidade da próxima Sprint)`);
  };

  return (
    <main style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem', fontFamily: 'sans-serif' }}>
      <header style={{ borderBottom: '2px solid #eee', marginBottom: '2rem' }}>
        <h1>🎓 V-Lab Educator Hub</h1>
      </header>

      <section>
        {loading && <p>Carregando dados do banco PostgreSQL...</p>}
        {error && <p style={{ color: 'red' }}>{error}</p>}
        
        {!loading && !error && (
          <StudentList 
            students={studentsData} 
            onStudentSelect={handleSelectStudent} 
          />
        )}
      </section>
    </main>
  );
}

export default App;