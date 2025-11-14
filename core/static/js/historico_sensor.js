function carregarTanques() {
      fetch('/api/tanques-do-usuario/')
        .then(response => response.json())
        .then(data => {
          const select = document.getElementById('tank');
          select.innerHTML = '<option value="">Selecione um tanque</option>';

          data.forEach(tanque => {
            const option = document.createElement('option');
            option.value = tanque.id;
            option.textContent = tanque.nome;
            select.appendChild(option);
          });
        })
        .catch(error => {
          console.error("Erro ao carregar tanques:", error);
        });
      document.addEventListener('DOMContentLoaded', function () {
        carregarTanques();
      });
carregarConteudo('/historico_sensor/', () => {
  if (document.getElementById('tank')) {
    carregarTanques();
    if (typeof inicializarHistoricoSensor === 'function') {
      inicializarHistoricoSensor(); 
    }
  } else {
    console.warn('Elemento #tank não encontrado após carregar a página.');
  }
});

document.addEventListener('DOMContentLoaded', function () {
      carregarTanques();
    });

    }