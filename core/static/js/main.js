function carregarConteudo(url) {
  fetch(url)
    .then(response => response.text())
    .then(html => {
      document.getElementById('conteudo-principal').innerHTML = html;
    })
    .catch(err => {
      console.error('Erro ao carregar conteúdo:', err);
    });
}
