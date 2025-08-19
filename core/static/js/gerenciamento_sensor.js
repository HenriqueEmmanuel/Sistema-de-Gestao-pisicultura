function mostrarTab(tab) {
    document.getElementById('sensores').style.display = (tab === 'sensores') ? 'block' : 'none';
    document.getElementById('dispositivos').style.display = (tab === 'dispositivos') ? 'block' : 'none';

    document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
    event.currentTarget.classList.add('active');
  }

  function abrirModalAdicionarSensor() {
    document.getElementById('modalAdicionarSensor').style.display = 'flex';
    carregarTanques();
  }

  function fecharModalAdicionarSensor() {
    document.getElementById('modalAdicionarSensor').style.display = 'none';
  }

  function carregarTanques() {
    fetch('/api/tanques-do-usuario/')
      .then(res => res.json())
      .then(tanques => {
        const select = document.getElementById('tank');
        select.innerHTML = '<option value="">Selecione um tanque</option>';
        tanques.forEach(tanque => {
          const option = document.createElement('option');
          option.value = tanque.id;
          option.textContent = tanque.nome;
          select.appendChild(option);
        });
      })
      .catch(err => {
        console.error("Erro ao carregar tanques:", err);
      });
  }

  function adicionarSensor() {
    const form = document.getElementById('formAdicionarSensor');
    const dados = {
      nome: form.nomeSensor.value.trim(),
      tipo: form.tipoSensor.value,
      tanque_id: form.tank.value,
      dispositivo_esp32_id: form.esp32Dispositivo.value,
      valor_minimo: form.valorMinimo.value || null,
      valor_maximo: form.valorMaximo.value || null,
      intervalo: form.intervalo.value,
      unidade_medida: form.unidadeMedida.value.trim(),
    };

    fetch('/api/adicionar-sensor/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
      },
      body: JSON.stringify(dados),
    })
    .then(res => {
      if (!res.ok) throw new Error('Erro ao adicionar sensor');
      return res.json();
    })
    .then(data => {
      if (data.success) {
        fecharModalAdicionarSensor();
        carregarConteudo('/gerenciamento_sensor/');  
        Swal.fire('Sucesso!', 'Sensor adicionado com sucesso.', 'success');
      } else {
        Swal.fire('Erro', data.error || 'Erro ao adicionar sensor', 'error');
      }
    })
    .catch(err => {
      console.error(err);
      Swal.fire('Erro', 'Erro ao adicionar sensor', 'error');
    });
  }

  function editarSensor(id) {
    alert('Editar sensor: ' + id);
  }

  function excluirSensor(id) {
    Swal.fire({
      title: 'Tem certeza?',
      text: 'Essa ação irá excluir o sensor.',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#3085d6',
      confirmButtonText: 'Sim, excluir',
      cancelButtonText: 'Cancelar'
    }).then(result => {
      if (result.isConfirmed) {
        fetch(`/api/excluir-sensor/${id}/`, {
          method: 'DELETE',
          headers: { 'X-CSRFToken': getCSRFToken() }
        })
        .then(res => {
          if (!res.ok) throw new Error('Erro ao excluir sensor');
          return res.json();
        })
        .then(data => {
          if (data.success) {
            carregarConteudo('/gerenciamento_sensor/');
            Swal.fire('Excluído!', 'Sensor removido com sucesso.', 'success');
          } else {
            Swal.fire('Erro', data.error || 'Erro ao excluir sensor', 'error');
          }
        })
        .catch(err => {
          console.error(err);
          Swal.fire('Erro', 'Erro ao excluir sensor', 'error');
        });
      }
    });
  }

  function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        return decodeURIComponent(cookie.substring(name.length + 1));
      }
    }
    return '';
  }