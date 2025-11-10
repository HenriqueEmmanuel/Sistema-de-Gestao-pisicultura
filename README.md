# 🐟 TilapiaControl — Sistema de Monitoramento e Análise Inteligente para Piscicultura

[![Django](https://img.shields.io/badge/Django-4.2-green?logo=django)](https://www.djangoproject.com/)
[![ESP32](https://img.shields.io/badge/ESP32-IoT-blue?logo=espressif)](https://www.espressif.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-yellow?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-orange.svg)](LICENSE)

---

## 🌎 Visão Geral

O **TilapiaControl** é um sistema modular voltado para o **monitoramento ambiental automatizado** e **análise inteligente de saúde de tilápias**, desenvolvido como parte de um **projeto acadêmico**.  
Ele combina **sensores físicos conectados a um ESP32** e um **módulo de reconhecimento de imagem via IA**, integrando os dados em um **painel web interativo** construído com **Django**.

---

## ⚙️ Funcionalidades Principais

- 🔬 **Monitoramento em tempo real** dos parâmetros de qualidade da água:
  - Temperatura  
  - pH  
  - Condutividade (TDS)  
  - Amônia  
  - Oxigênio Dissolvido
  - Amônia
  - Nitrito/Nitrato
  - Salinidade

- 🤖 **Análise Inteligente de Imagens** de tilápias, com classificação automática:
  - Saudável ✅  
  - Com anomalias ⚠️  

- 📊 **Painel de Controle Responsivo**
  - Visualização de gráficos e histórico de medições  
  - Filtro por tanque, período e parâmetro  
  - Carregamento dinâmico via AJAX  

- 📩 **Sistema de Alertas**
  - Envio automático de notificações por **e-mail** ou **SMS** em caso de parâmetros fora do limite configurado  

- 🔒 **Autenticação e Perfis de Usuário**
  - Cadastro, login e configurações personalizadas  
  - Escolha do método de notificação preferido  

---

## 🧠 Arquitetura do Sistema

+---------------------+          +----------------------+
|      ESP32 +        |  HTTP    |   Servidor Django    |
|   Sensores (IoT)    +--------->+   API REST / Views   |
| pH | Temp | TDS ... |          +----------+-----------+
+---------------------+                     |
                                            |
                                            v
                               +-----------------------------+
                               |       Banco de Dados        |
                               |     SQLite / PostgreSQL     |
                               +-------------+---------------+
                                             |
                                             v
                                  +--------------------+
                                  |   Interface Web    |
                                  |  (Dashboard AJAX)  |
                                  +--------------------+
---


## 💾 Instalação e Configuração

### 1️⃣ Clonar o repositório
```bash
git clone [https://github.com/seu-usuario/TilapiaControl.git](https://github.com/HenriqueEmmanuel/Sistema-de-Gestao-pisicultura.git)
cd TilapiaControl

2️⃣ Criar e ativar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows

3️⃣ Instalar dependências
pip install -r requirements.txt

4️⃣ Criar arquivo .env

Crie um arquivo .env na raiz com as variáveis de ambiente:

SECRET_KEY=sua_chave_django
DEBUG=True
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu_email@gmail.com
EMAIL_HOST_PASSWORD=sua_senha_app

5️⃣ Migrar banco de dados
python manage.py makemigrations
python manage.py migrate

6️⃣ Rodar servidor
python manage.py runserver

Acesse em:
👉 http://127.0.0.1:8000/

🧪 Testes de Envio de Dados (ESP32)

O ESP32 envia leituras de sensores via requisições HTTP POST para a API do Django:

// Exemplo de endpoint
String server = "http://SEU_IP:8000/api/dados/";


📬 Sistema de Alerta

O sistema monitora continuamente os valores de sensores.
Caso um parâmetro ultrapasse o limite configurado, é enviado um alerta automático via e-mail ou SMS, conforme a preferência do usuário.


🧰 Tecnologias Utilizadas
| Categoria          | Tecnologias                              |
| ------------------ | ---------------------------------------- |
| Backend            | Django, Django REST Framework            |
| IoT                | ESP32, Arduino                           |
| Banco de Dados     | SQLite / PostgreSQL                      |
| Frontend           | HTML5, CSS3, JavaScript (AJAX, Chart.js) |
| IA                 | Gemini API / Modelos de Classificação    |
| Notificações       | SMTP (e-mail) / SMS API                  |
| Controle de Versão | Git + GitHub                             |



📜 Licença

Este projeto é distribuído sob a licença MIT
.
Sinta-se livre para usar, modificar e distribuir com os devidos créditos.


👨‍💻 Autores

Henrique Emmanuel

