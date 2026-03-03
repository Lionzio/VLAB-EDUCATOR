/**
 * Componente Raiz da Aplicação (Entrypoint Visual).
 * Seguindo a metodologia Atomic Design, este arquivo não deve conter lógica de negócio
 * complexa ou estilos hardcoded. Ele servirá como o orquestrador que renderiza 
 * as nossas "Pages" (Páginas) dinâmicas.
 */

function App() {
  return (
    <main>
      {/* Futuramente, substituiremos este conteúdo estático pelo nosso sistema de roteamento.
        Exemplo do que virá nas próximas Sprints:
        <Routes>
           <Route path="/" element={<HomePage />} />
           <Route path="/generate" element={<GeneratorPage />} />
        </Routes>
      */}
      
      <div style={{ padding: '2rem', fontFamily: 'system-ui, sans-serif' }}>
        <h1>🎓 V-Lab Educator</h1>
        <p>Ambiente React inicializado com sucesso.</p>
        <p>
          <em>O terreno está limpo e pronto para a criação dos Átomos, Moléculas e Organismos.</em>
        </p>
      </div>
    </main>
  )
}

export default App