

    //gerenciar tanque.html
  function enviarFormulario() {
    const form = document.getElementById('form-configuracoes');
    const formData = new FormData(form);
    const data = {};

    formData.forEach((value, key) => {
      data[key] = value;
    });

    fetch(form.action, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
      },
      body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
      if (data.sucesso) {
        alert("Alterações salvas com sucesso!");
        voltarParaTanques();
      } else {
        alert("Erro ao salvar: " + (data.erro || "Erro desconhecido"));
      }
    })
    .catch(error => {
      console.error("❌ Erro na requisição:", error);
      alert("Erro ao se comunicar com o servidor.");
    });
  }


function abrirModalParametros(botao) {
    const tanqueId = botao.getAttribute('data-tanque-id');
    const modal = document.getElementById('modal-parametros');
    modal.style.display = 'flex';

    fetch(`/get_parametros_personalizados/${tanqueId}/`)
        .then(res => res.json())
        .then(data => {
            for (let key in data) {
                let input = modal.querySelector(`[name="${key}"]`);
                if (input) input.value = data[key];
            }
        })
        .catch(err => console.error("Erro ao carregar parâmetros:", err));

    document.getElementById('btnSalvarParametros').onclick = () => salvarParametrosPersonalizados(tanqueId);
}

document.getElementById('btnFecharModal').onclick = () => {
    document.getElementById('modal-parametros').style.display = 'none';
};

function salvarParametrosPersonalizados(tanqueId) {
    const form = document.getElementById('form-parametros');
    const formData = new FormData(form); 
    const formDataObj = {};
    formData.forEach((value, key) => formDataObj[key] = value);

fetch(`/salvar_parametros_modal/${tanqueId}/`, {
    method: 'POST',
    headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(formDataObj)
})

    .then(response => response.json())
    .then(result => {
        if(result.sucesso) {
            alert('Parâmetros salvos!');
           
        } else {
            alert('Erro: ' + result.erro);
        }
    })
    .catch(err => console.error(err));
}
