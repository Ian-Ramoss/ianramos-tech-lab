# 🤖 Bot de Escala de Trabalho

Projeto pessoal para automatizar controle de escala de trabalho, consultas rápidas via Telegram Bot.

---

# 📌 Objetivo do Projeto

Este sistema foi criado para resolver um problema real:

- Controlar dois trabalhos com escalas diferentes
- Saber onde trabalha hoje, amanhã ou qualquer data futura
- Visualizar mês, semana ou ano inteiro
- Receber alertas
- Automatizar agenda pessoal

---

# 🧠 Regra da Escala

## Trabalho A
- Plantão de **24 horas**
- Regra: **24x48**
- Exemplo:
  - Entra domingo 09:00
  - Sai segunda 09:00

## Trabalho B
- Plantão de **12 horas**
- Ocorre sempre no **segundo dia de folga** do Trabalho A

## Resultado do ciclo

Exemplo:

| Dia | Escala |
|-----|--------|
| Domingo | Trabalho A |
| Segunda | Folga |
| Terça | Trabalho B |
| Quarta | Trabalho A |
| Quinta | Folga |
| Sexta | Trabalho B |

E assim sucessivamente.

---

# 🚀 Funcionalidades do Bot Telegram

Comandos disponíveis:

| Comando | Função |
|--------|-------|
| /start | Inicia bot |
| /hoje | Escala de hoje |
| /amanha | Escala de amanhã |
| /ontem | Escala de ontem |
| /semana | Próximos 7 dias |
| /mes | Escala do mês atual |
| /mes 3 2026 | Março de 2026 |
| /ano | Escala do ano atual |

---

# 🛠️ Tecnologias Utilizadas

## Python Version
- Python 3.10+

## Bibliotecas

```bash
python-telegram-bot
pytz
APScheduler