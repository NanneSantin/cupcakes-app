// Fecha automaticamente as mensagens (alertas) após 5 segundos
document.querySelectorAll(".alert-dismissible").forEach(function (alerta) {
  setTimeout(function () {
    bootstrap.Alert.getOrCreateInstance(alerta).close();
  }, 5000);
});