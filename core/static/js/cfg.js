document.getElementById('form-configuracoes').addEventListener('submit', function (e) {
    e.preventDefault();

    const form = e.target;
    const formData = new FormData(form);

    formData.set('notificacoes_push', document.getElementById('notificacoes_push').checked.toString());
    formData.set('notificacoes_email', document.getElementById('notificacoes_email').checked.toString());
    formData.set('alerta_agua', document.getElementById('alerta_agua').checked.toString());
    formData.set('lembrete_alimentacao', document.getElementById('lembrete_alimentacao').checked.toString());
    formData.set('backup_auto', document.getElementById('backup_auto').checked.toString());
    formData.set('dois_fatores', document.getElementById('dois_fatores').checked.toString());

    fetch('/salvarcfg/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert(data.mensagem);
    })
    .catch(() => {
        alert("Erro ao salvar!");
    });
});
