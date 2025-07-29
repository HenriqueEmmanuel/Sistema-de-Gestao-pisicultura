

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
