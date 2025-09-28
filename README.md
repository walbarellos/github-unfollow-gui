# GitHub Unfollow Manager — GUI
<img width="1896" height="806" alt="Captura de imagem_20250928_133602" src="https://github.com/user-attachments/assets/4fbd1f24-969b-4749-9527-1249326fd827" />

Ferramenta web para **gerenciar seguidores no GitHub**, permitindo identificar:
- Quem você segue mas **não te segue de volta**.
- Quem segue você mas você **não segue de volta**.
- Seus **seguidores mútuos**.

Com uma interface gráfica simples, é possível **aplicar filtros, marcar usuários e executar unfollow seletivo**.  
Inclui **modo seguro (dry-run)**, cache temporário e logs de auditoria em JSON.

---

## ✨ Como funciona

1. O sistema usa a **API oficial do GitHub** com o seu **token pessoal (PAT)**.  
2. Ao abrir a interface em [http://127.0.0.1:5000](http://127.0.0.1:5000):
   - Ele busca sua lista de **seguindo** e **seguidores**.
   - Compara as listas para descobrir **quem não retribui**.
   - Exibe tudo em tabelas interativas com **filtros, busca e ordenação**.
3. Você pode:
   - Filtrar por nome, localização, tipo de conta (User/Organization) e número mínimo de seguidores.
   - Marcar usuários com checkbox.
   - Clicar em **Unfollow Selecionados**.
4. O comportamento depende da configuração:
   - **DRY_RUN=true** → apenas simula, não dá unfollow real. Cria um log em `logs/`.
   - **DRY_RUN=false** → envia requisição real de unfollow para o GitHub.

---

## 🛠️ Instalação

### 1. Clone o repositório
```bash
git clone https://github.com/SEU_USUARIO/github-unfollow-gui
cd github-unfollow-gui
```
---

## 👨‍💻 Autor & Créditos

- **Willian Albarello** — idealizador, integração com projetos privados, e Programação Principal.  
- ~~Assistente AI (ChatGPT) — apoio em engenharia, documentação e refino do código.~~

**Nota do Editor (Willian):** ~~Meu papel de Programador Sênior e Idealizador foi mantido.~~

## 📜 Licença

Distribuído sob a **MIT License**. Veja o arquivo `LICENSE` para mais detalhes.

```text
MIT License

Copyright (c) 2025 Willian Albarello

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas!
Abra um **issue** ou envie um **pull request** com melhorias, correções ou novas funcionalidades.

---
