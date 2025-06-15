tankmanage.tsx
dash.html:
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Dashboard Aquicultura</title>
  {% load static %}
  <link rel="stylesheet" href="{% static 'css/dash.css' %}">
  
</head>
<body>

  <header class="navbar">
    🐟 TilapiaControl
  </header>

  <div class="container">
    <aside class="sidebar">
      <nav>
        <ul class="menu">
          <li><a href="#" data-url="{% url 'dashboard' %}" onclick="carregarConteudo(this.dataset.url); return false;">🏠 Dashboard</a></li>
          <li><a href="#" data-url="{% url 'tank' %}" onclick="carregarConteudo(this.dataset.url); return false;">📦 Gerenciar Tanques</a></li>
          <li><a href="#" data-url="{% url 'analise' %}" onclick="carregarConteudo(this.dataset.url); return false;">📋 Histórico Análises</a></li>
          <li><a href="#" data-url="{% url 'historico_sensor' %}" onclick="carregarConteudo(this.dataset.url); return false;">🧾 Histórico Sensores</a></li>
          <li><a href="#" data-url="{% url 'gerenciamento_sensor' %}" onclick="carregarConteudo(this.dataset.url); return false;">⚙️ Gerenciar Sensores</a></li>
        </ul>
      </nav>
    </aside>

    <main aria-label="Conteúdo Principal">
      <!-- Seu conteúdo atual, alertas, indicadores, gráficos... -->
      <section class="alert" aria-label="Alertas do Sistema">
        <strong>Alertas do Sistema</strong>
        <div class="alert-item">
          <span>pH fora do ideal: 6.8</span>
          <span class="badge warning">pH</span>
        </div>
        <div class="alert-item">
          <span>Nível de amônia alto: 0.35 mg/L</span>
          <span class="badge danger">Amônia</span>
        </div>
        <div class="alert-item">
          <span>Temperatura fora do ideal: 25.8°C</span>
          <span class="badge warning">Temperatura</span>
        </div>
      </section>

      <section class="grid grid-4" aria-label="Indicadores Principais">
        <!-- indicadores aqui -->
      </section>

      <section class="charts" aria-label="Gráficos de monitoramento">
        <!-- gráficos aqui -->
      </section>
    </main>
  </div>

</body>
</html>

dash.css:
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f9fafb;
  color: #1f2937;
}

header {
  padding: 1rem;
  background-color: #ffffff;
  border-bottom: 1px solid #d1d5db;
}

h1 {
  font-size: 2rem;
  font-weight: bold;
  margin: 0;
}

p.description {
  color: #4b5563;
  margin-top: 0.25rem;
}

.layout {
  display: flex;
  min-height: calc(100vh - 80px); /* altura total menos header */
}

.sidebar {
  width: 240px;
  background-color: #ffffff;
  padding: 1rem;
  border-right: 1px solid #e5e7eb;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.05);
  flex-shrink: 0;
  
}

.menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.menu li {
  margin-bottom: 0.75rem;
}

.menu a {
  text-decoration: none;
  color: #1f2937;
  font-weight: 500;
  display: block;
  padding: 0.5rem;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.menu a:hover {
  background-color: #e5e7eb;
}

main {
  flex-grow: 1;
  padding: 1rem;
}

.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgb(0 0 0 / 0.1);
  padding: 1rem;
  margin-bottom: 1.5rem;
}

.alert {
  border: 1px solid #fbbf24;
  background-color: #fef3c7;
  color: #b45309;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.alert-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
}

.badge {
  padding: 0.15rem 0.5rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}

.badge.warning {
  background-color: #fbbf24;
  color: #92400e;
}

.badge.danger {
  background-color: #dc2626;
  color: white;
}

.grid {
  display: grid;
  gap: 1rem;
}

.grid-4 {
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
}

.indicator {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.indicator-info {
  font-size: 1.25rem;
  font-weight: bold;
}

.indicator-label {
  font-size: 0.875rem;
  color: #6b7280;
}

.indicator-ideal {
  font-size: 0.75rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

.charts {
  display: grid;
  gap: 1rem;
  grid-template-columns: 1fr 1fr;
}

.chart-placeholder {
  height: 300px;
  background-color: #e5e7eb;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  font-style: italic;
  user-select: none;
}
