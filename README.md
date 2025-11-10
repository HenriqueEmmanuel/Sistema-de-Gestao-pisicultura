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

