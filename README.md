# Space Jumper Adventure (Platformer) 🚀

> **Projeto Final de Python** > **Biblioteca:** PgZero

## 📝 Descrição

Este é um jogo de plataforma clássico onde o herói deve pular entre plataformas, evitar inimigos patrulheiros e sobreviver o maior tempo possível. O projeto foi desenvolvido com foco em:
* Física de gravidade;
* Animações de sprite (idle/run);
* Gerenciamento de estados (Menu, Jogo, Game Over).

---

## ⚙️ Requisitos de Instalação

Para rodar este jogo, você precisa ter o Python instalado.

1. **Python 3** (Certifique-se de adicioná-lo ao PATH durante a instalação).
2. Instale a biblioteca **PgZero** via terminal:

```bash
pip install pgzero
```

```bash
MeuProjeto/
 │
 ├── main.py            <-- O código fonte do jogo
 ├── README.md          <-- Este arquivo
 │
 ├── images/            <-- Pasta OBRIGATÓRIA para imagens (.png)
 │    ├── hero_idle1.png
 │    ├── hero_idle2.png
 │    ├── hero_run1.png
 │    ├── hero_run2.png
 │    ├── enemy1.png
 │    ├── enemy2.png
 │    └── (Outros assets visuais)
 │
 └── sounds/            <-- Pasta OBRIGATÓRIA para áudio
      ├── jump.wav      <-- Som curto para o pulo
      └── music.mp3     <-- Música de fundo
