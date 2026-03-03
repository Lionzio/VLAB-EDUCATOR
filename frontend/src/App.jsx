/**
 * Componente Raiz (Orquestrador Principal).
 * Responsável pelo fluxo da aplicação: Listagem -> Formulário -> Resultado.
 * Implementa boas práticas de React: tratamento de erros granular,
 * loading states independentes e limpeza de estado (cleanup).
 */
import React, { useState, useEffect } from 'react';
import { api } from './services/api';

// Importação dos Componentes do Atomic Design
import StudentList from './components/organisms/StudentList';
import GeneratorForm from './components/organisms/GeneratorForm';
import Button from './components/atoms/Button';

function App() {
  // 1. Estados Globais da Aplicação
  const [studentsData, setStudentsData] = useState([]);
  
  // Estados de Carregamento Isolados (Melhora a UX)
  const [loadingDb, setLoadingDb] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  
  // Estados de Controle de Fluxo
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [generatedResult, setGeneratedResult] = useState(null);
  
  // Estado para feedback de erros globais
  const [globalError, setGlobalError] = useState(null);

  // 2. Efeito de Inicialização (Busca os alunos no banco de dados)
  useEffect(() => {
    // Definimos uma função assíncrona isolada dentro do useEffect (Boa prática)
    const fetchStudents = async () => {
      try {
        const res = await api.get('/students');
        setStudentsData(res.data);
      } catch (err) {
        console.error("Erro na busca de alunos:", err);
        setGlobalError("Não foi possível conectar ao banco de dados PostgreSQL. Verifique se o Backend está rodando.");
      } finally {
        setLoadingDb(false);
      }
    };

    fetchStudents();
  }, []);

  // 3. Handlers (Ações disparadas por eventos)
  const handleGenerate = async (formData) => {
    // Reseta estados antes da nova tentativa
    setIsGenerating(true);
    setGeneratedResult(null);
    setGlobalError(null);

    try {
      const response = await api.post('/generate', formData);
      setGeneratedResult(response.data);
    } catch (error) {
      console.error("Falha na geração:", error);
      
      // Tratamento de erro específico da API via Axios
      if (error.response && error.response.data && error.response.data.erro) {
         setGlobalError(`Falha da API: ${error.response.data.erro}`);
      } else {
         setGlobalError("Falha de rede ao tentar gerar o conteúdo. Tente novamente.");
      }
    } finally {
      setIsGenerating(false);
    }
  };

  const handleResetWorkflow = () => {
    // Retorna o usuário ao estado inicial (Lista de Alunos) de forma limpa
    setSelectedStudent(null);
    setGeneratedResult(null);
    setGlobalError(null);
  };

  // 4. Renderização (Visão)
  return (
    <main style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem', fontFamily: 'system-ui, sans-serif' }}>
      
      {/* Header Fixo */}
      <header style={{ borderBottom: '2px solid #eaeaea', paddingBottom: '1rem', marginBottom: '2rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1 style={{ margin: 0, color: '#333' }}>🎓 V-Lab Educator Hub</h1>
        
        {/* Renderização Condicional do Botão de Voltar */}
        {selectedStudent && (
          <Button onClick={handleResetWorkflow} variant="secondary">
            ← Voltar para a Lista
          </Button>
        )}
      </header>

      {/* Banner de Erro Global (UX Defensiva) */}
      {globalError && (
        <div style={{ backgroundColor: '#ffeef0', color: '#d32f2f', padding: '1rem', borderRadius: '4px', marginBottom: '2rem', border: '1px solid #f5c2c7' }}>
          <strong>⚠️ Atenção:</strong> {globalError}
        </div>
      )}

      <section>
        {/* Fluxo 1: Listagem de Alunos */}
        {!selectedStudent && (
          loadingDb ? (
             <div style={{ textAlign: 'center', padding: '2rem' }}>
                <p>⏳ Carregando dados do PostgreSQL...</p>
             </div>
          ) : (
            <StudentList 
              students={studentsData} 
              onStudentSelect={setSelectedStudent} 
            />
          )
        )}

        {/* Fluxo 2: Formulário de Geração */}
        {selectedStudent && !generatedResult && (
          <GeneratorForm 
            student={selectedStudent} 
            onSubmit={handleGenerate} 
            isLoading={isGenerating} 
          />
        )}

        {/* Fluxo 3: Exibição do Resultado Final (JSON Formatado) */}
        {generatedResult && (
          <div style={{ backgroundColor: '#f8f9fa', padding: '2rem', borderRadius: '8px', marginTop: '1rem', border: '1px solid #dee2e6' }}>
            <h2 style={{ color: '#198754', marginTop: 0 }}>✅ {generatedResult.mensagem}</h2>
            
            <p style={{ fontSize: '0.9rem', color: '#6c757d', marginBottom: '1.5rem' }}>
              <strong>Origem dos Dados:</strong> {generatedResult.fonte}
            </p>
            
            <div style={{ backgroundColor: '#212529', color: '#f8f9fa', padding: '1.5rem', borderRadius: '6px', overflowX: 'auto' }}>
               <pre style={{ margin: 0, fontSize: '0.95rem' }}>
                 {JSON.stringify(generatedResult.dados_gerados, null, 2)}
               </pre>
            </div>
          </div>
        )}
      </section>
    </main>
  );
}

export default App;