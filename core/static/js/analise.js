
// Exemplo simples de chamada ao clicar na sidebar
document.querySelectorAll('.menu a').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    const url = link.getAttribute('href'); // ou data-url
    carregarConteudo(url);  // função que você já implementou para fetch + atualizar main
  });
});


async function carregarConteudo(url) {
  try {
    const response = await fetch(url);
    if (!response.ok) throw new Error('Erro ao carregar o conteúdo');
    const html = await response.text();

    // Inserir só o conteúdo da página (que deve ser só o <main> do novo conteúdo)
    document.querySelector('main').innerHTML = html;

    // Após inserir o conteúdo, reativa os controles da câmera:
    ativarAnaliseEmTempoReal();

  } catch (err) {
    console.error(err);
    alert('Erro ao carregar conteúdo');
  }
}

function ativarAnaliseEmTempoReal() {
  const video = document.getElementById('video');
  const canvas = document.getElementById('canvas');
  const overlay = document.getElementById('overlay');
  const resultDiv = document.getElementById('result');
  let stream = null;
  let auto = false;
  let analyzing = false;
  let autoInterval;

  document.getElementById('startBtn').onclick = async () => {
    stream = await navigator.mediaDevices.getUserMedia({ video: true });
    video.srcObject = stream;
  };

  document.getElementById('stopBtn').onclick = () => {
    if(stream) {
      stream.getTracks().forEach(track => track.stop());
      video.srcObject = null;
      stream = null;
    }
    clearInterval(autoInterval);
  };

  function showResult(status, confidence, details) {
    resultDiv.innerHTML = `
      <p>Status: <span class="status ${status}">${status === 'healthy' ? 'Saudável' : 'Anomalia'}</span></p>
      <p>Confiança: ${confidence}%</p>
      <ul>${details.map(d => `<li>${d}</li>`).join('')}</ul>
      <p class="text-sm">${new Date().toLocaleString('pt-BR')}</p>
    `;
  }

  async function analyze() {
    if (!stream || analyzing) return;
    analyzing = true;
    overlay.style.display = 'flex';
    await new Promise(res => setTimeout(res, 1500));
    const healthy = Math.random() > 0.3;
    showResult(
      healthy ? 'healthy' : 'anomaly',
      Math.round((Math.random() * 0.3 + 0.7) * 100),
      healthy ? ["Peixe saudável", "Coloração normal"] : ["Anomalia detectada", "Movimento incomum"]
    );
    overlay.style.display = 'none';
    analyzing = false;
  }

  document.getElementById('analyzeBtn').onclick = analyze;

  document.getElementById('toggleAutoBtn').onclick = () => {
    auto = !auto;
    if (auto) {
      autoInterval = setInterval(analyze, 10000);
    } else {
      clearInterval(autoInterval);
    }
  };
}
