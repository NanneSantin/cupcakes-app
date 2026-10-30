// ===================================================================
// Mensagens
// ===================================================================

// Fecha automaticamente as mensagens (alertas) após 5 segundos
document.querySelectorAll(".alert-dismissible").forEach(function (alerta) {
  setTimeout(function () {
    bootstrap.Alert.getOrCreateInstance(alerta).close();
  }, 5000);
});

// Mostra um aviso rápido no canto da tela (sem recarregar a página)
function mostrarAviso(mensagem, tipo) {
  const aviso = document.createElement("div");
  aviso.className = "toast align-items-center border-0 text-bg-" + (tipo || "success");
  aviso.setAttribute("role", "status");
  aviso.innerHTML =
    '<div class="d-flex"><div class="toast-body"></div>' +
    '<button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Fechar"></button></div>';
  aviso.querySelector(".toast-body").textContent = mensagem;
  document.getElementById("avisos").appendChild(aviso);
  aviso.addEventListener("hidden.bs.toast", function () { aviso.remove(); });
  new bootstrap.Toast(aviso, { delay: 2500 }).show();
}

// Atualiza o número do carrinho no menu
function atualizarBadgeCarrinho(quantidade) {
  const badge = document.getElementById("badge-carrinho");
  if (!badge) return;
  badge.textContent = quantidade;
  badge.classList.toggle("d-none", !quantidade);
}

// Envia um formulário em segundo plano e devolve a resposta em JSON.
// Erros de validação (400) também voltam em JSON, com a mensagem para o usuário.
async function enviarFormulario(form) {
  const resposta = await fetch(form.action, {
    method: "POST",
    body: new FormData(form),
    headers: { "X-Requested-With": "fetch" },
  });
  const tipo = resposta.headers.get("Content-Type") || "";
  if (!tipo.includes("application/json")) throw new Error("Erro " + resposta.status);
  const dados = await resposta.json();
  dados.ok = resposta.ok;
  return dados;
}

// ===================================================================
// Seletor de quantidade (botões − e +)
// ===================================================================
document.addEventListener("click", function (evento) {
  const botao = evento.target.closest(".seletor-qtd [data-acao]");
  if (!botao) return;

  const campo = botao.closest(".seletor-qtd").querySelector("input");
  const minimo = parseInt(campo.min) || 1;
  const maximo = parseInt(campo.max) || 99;
  let valor = parseInt(campo.value) || minimo;

  valor += botao.dataset.acao === "aumentar" ? 1 : -1;
  valor = Math.min(maximo, Math.max(minimo, valor));

  if (String(valor) !== campo.value) {
    campo.value = valor;
    campo.dispatchEvent(new Event("change", { bubbles: true }));
  }
});

// ===================================================================
// Adicionar ao carrinho sem sair do lugar (vitrine e detalhe)
// ===================================================================
document.addEventListener("submit", async function (evento) {
  const form = evento.target.closest(".form-adicionar");
  if (!form) return;
  evento.preventDefault();

  const botao = form.querySelector("[type=submit]");
  botao.disabled = true;
  try {
    const dados = await enviarFormulario(form);
    mostrarAviso(dados.mensagem, dados.tipo);
    if (dados.ok) {
      atualizarBadgeCarrinho(dados.qtd_carrinho);
      form.querySelector("input[name=quantidade]").value = 1;
    }
  } catch (erro) {
    form.submit(); // se algo falhar, envia do jeito tradicional
  } finally {
    botao.disabled = false;
  }
});

// ===================================================================
// Carrinho: salva a quantidade automaticamente e recalcula os valores
// ===================================================================
const esperas = new WeakMap();

document.addEventListener("change", function (evento) {
  const form = evento.target.closest(".form-atualizar");
  if (!form) return;

  // Espera um instante para juntar vários cliques seguidos em um único envio
  clearTimeout(esperas.get(form));
  esperas.set(form, setTimeout(async function () {
    try {
      const dados = await enviarFormulario(form);
      if (dados.quantidade) form.querySelector("input[name=quantidade]").value = dados.quantidade;
      if (dados.mensagem) mostrarAviso(dados.mensagem, dados.tipo);
      if (!dados.ok) return;
      document.querySelector('[data-subtotal="' + form.dataset.produto + '"]').textContent = dados.subtotal;
      document.getElementById("total-carrinho").textContent = dados.total;
      atualizarBadgeCarrinho(dados.qtd_carrinho);
    } catch (erro) {
      form.submit();
    }
  }, 400));
});

// Se a pessoa digitar a quantidade e apertar Enter, salva sem recarregar
document.addEventListener("submit", function (evento) {
  const form = evento.target.closest(".form-atualizar");
  if (!form) return;
  evento.preventDefault();
  form.querySelector("input[name=quantidade]").dispatchEvent(new Event("change", { bubbles: true }));
});

// ===================================================================
// Painel do admin: salva o status assim que uma opção é escolhida
// ===================================================================
document.addEventListener("change", function (evento) {
  const select = evento.target.closest(".form-status select");
  if (!select) return;

  // Cancelar não pode ser desfeito, então pede confirmação
  if (select.value === "Cancelado" &&
    !confirm("Cancelar este pedido? Os produtos voltam ao estoque e não será possível reabrir.")) {
    select.value = select.dataset.atual;
    return;
  }
  select.form.submit();
});
