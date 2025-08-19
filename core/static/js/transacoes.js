function abrirModalTransacao() {
    document.getElementById("modalTransacao").style.display = "block";
    carregarTanques();
  }

  function fecharModalTransacao() {
    document.getElementById("modalTransacao").style.display = "none";
  }

  function atualizarCategorias() {
    let tipo = document.getElementById("tipo").value;
    document.getElementById("despesa-container").style.display = (tipo === "despesa") ? "block" : "none";
    document.getElementById("receita-container").style.display = (tipo === "receita") ? "block" : "none";
  }

  function carregarTanques() {
    fetch('/api/tanques-do-usuario/')
      .then(res => res.json())
      .then(tanques => {
        const select = document.getElementById('tanque');
        select.innerHTML = '<option value="">Geral</option>';
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

  function atualizarSubcategorias() {
    let categoria = document.getElementById("categoria").value;
    let subcategoria = document.getElementById("subcategoria");
    let subcategoriaContainer = document.getElementById("subcategoria-container");

    subcategoria.innerHTML = "";
    let opcoes = [];

    if (categoria === "custo_variavel") {
      opcoes = ["Ração", "Alevinos", "Vacina/Medicamentos", "Energia Elétrica", "Transporte", "Insumos"];
    } else if (categoria === "custo_fixo") {
      opcoes = ["Manutenção de equipamentos", "Manutenção de instalações"];
    } else if (categoria === "despesa_operacional") {
      opcoes = ["Salários/Encargos", "Impostos/Taxas", "Despesas administrativas", "Outros"];
    }

    if (opcoes.length > 0) {
      opcoes.forEach(o => {
        let opt = document.createElement("option");
        opt.value = o.toLowerCase().replace(/\s+/g, "_");
        opt.textContent = o;
        subcategoria.appendChild(opt);
      });
      subcategoriaContainer.style.display = "block";
      subcategoria.setAttribute("required", "required");
    } else {
      subcategoriaContainer.style.display = "none";
      subcategoria.removeAttribute("required");
    }
  }

  function calcularValorTotalReceita() {
    let qtd = parseFloat(document.getElementById("quantidade-receita").value) || 0;
    let preco = parseFloat(document.getElementById("preco-unitario-receita").value) || 0;
    document.getElementById("valor-total-receita").value = (qtd * preco).toFixed(2);
  }

  function abrirModalRelatorio() {
    document.getElementById("modalRelatorio").style.display = "block";
  }

  function fecharModalRelatorio() {
    document.getElementById("modalRelatorio").style.display = "none";
  }

  function mostrarDatasPersonalizadas() {
    const periodo = document.getElementById("periodo-relatorio").value;
    const divDatas = document.getElementById("datas-personalizadas");
    if (periodo === "personalizado") {
      divDatas.style.display = "block";
    } else {
      divDatas.style.display = "none";
    }

  }

  function gerarRelatorio() {
    const formato = document.getElementById("formato-relatorio").value;
    const periodo = document.getElementById("periodo-relatorio").value;
    const dataInicio = document.getElementById("data-inicio").value;
    const dataFim = document.getElementById("data-fim").value;

    let url = `/exportar-transacoes/?formato=${formato}&periodo=${periodo}`;
    if (periodo === 'personalizado') {
        url += `&data_inicio=${dataInicio}&data_fim=${dataFim}`;
    }

    window.open(url, '_blank');

    fecharModalRelatorio();
}
