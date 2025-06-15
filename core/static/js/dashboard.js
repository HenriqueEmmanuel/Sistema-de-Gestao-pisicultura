    function carregarConteudo(url) {
      fetch(url)
        .then(response => response.text())
        .then(html => {
          const main = document.querySelector('main');
          if (main) {
            main.innerHTML = html;
          } else {
            const novoMain = document.createElement('main');
            novoMain.innerHTML = html;
            document.querySelector('.layout').appendChild(novoMain);
          }
        })
        .catch(error => console.error('Erro ao carregar conteúdo:', error));
    }
