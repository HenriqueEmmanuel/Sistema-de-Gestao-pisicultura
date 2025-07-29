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

      // Procurar por tags <script data-dinamico> dentro do HTML carregado
      const divTemporaria = document.createElement('div');
      divTemporaria.innerHTML = html;

      const scripts = divTemporaria.querySelectorAll('script[data-dinamico]');
      scripts.forEach(oldScript => {
        const newScript = document.createElement('script');
        if (oldScript.src) {
          newScript.src = oldScript.src;
        } else {
          newScript.textContent = oldScript.textContent;
        }
        document.body.appendChild(newScript);
      });

    })
    .catch(error => console.error('Erro ao carregar conteúdo:', error));
}
