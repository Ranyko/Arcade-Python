# Central de Jogos de Tabuleiro - Interface KivyMD

Este repositório contém o front-end em KivyMD e a integração com as regras orientadas a objetos desenvolvidas na Fase 1 para dois jogos clássicos: **Jogo da Velha** e **Connect 4 (Lig 4)**.

O projeto foi construído seguindo o padrão de projeto **MVC (Model-View-Controller)** para desacoplar totalmente a lógica de visualização (KivyMD) das regras puras de jogo.

---

## 👤 Desenvolvedor: Raniery Chiarelli


---

## 🚀 Como Instalar e Rodar o Aplicativo

### Pré-requisitos
* Python 3.10 ou superior instalado na máquina.
* Gerenciador de pacotes `pip`.

### Instalação Passo a Passo

1. **Clonar o Repositório:**
   ```bash
   git clone https://github.com/Ranyko/Arcade-Python.git
   cd Arcade-Python
   ```

2. **Criar e Ativar Ambiente Virtual:**
   * No Windows:
     ```powershell
     python -m venv .venv
     .venv\Scripts\activate
     ```
   * No Linux / macOS:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Instalar Dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Executar o Jogo:**
   ```bash
   python main.py
   ```

---

## 🕹️ Funcionalidades e Telas Implementadas

O aplicativo contém uma experiência visual de jogo, incluindo:
1. **Menu Principal (`MenuScreen`):** Tela inicial com suporte a **Alternância de Tema Claro/Escuro** em tempo real e detecção automática de partidas salvas.
2. **Seleção de Jogo (`GameSelectScreen`):** Interface intuitiva em forma de cards para escolher entre Jogo da Velha ou Connect 4 e, futuramente, outros jogos que possam ser implementados
3. **Configuração de Partida (`ConfigScreen`):** Permite inserir o nome dos jogadores, escolher a cor das peças de cada um e ativar o modo de jogo **Contra Computador (IA)** que segue uma base simples sem Machine Learning.
4. **Tabuleiro (`BoardScreen`):** Visualização dinâmica das jogadas com gravidade automática no Connect 4. Conta com um painel de status que exibe a vez de quem joga com o indicador da cor ativa . Inclui um botão para **Salvar Partida** a qualquer momento.
5. **Tela de Resultado (`ResultScreen`):** Apresentação do vencedor ou empate com animações e ícones (troféu/aperto de mãos).

---

## 🤖 Uso de Inteligência Artificial

* **Ferramenta:** Antigravity (Powered by Gemini 3.5 Flash)
* **Finalidade:** Auxílio no refinamento visual dos componentes KivyMD, depuração da assinatura de métodos de redesenho reativos no canvas do Kivy, estruturação da lógica de melhor jogada para o oponente IA e serialização em formato JSON para salvar/carregar partidas em andamento.
* **Compreensão:** Todo o código gerado foi revisado, refatorado e compreendido, com a IA sendo uma ferramenta essencial para o aprendizado do Front End.

---

## 📐 Estrutura do Projeto (MVC)

* `main.py`: Inicializa o aplicativo KivyMD, configura o `ScreenManager` e define as cores básicas do tema.
* `src/`: Lógica interna do jogo e tabuleiro (intacta e independente de UI).
* `app/`: Contém os componentes e a lógica da interface do usuário.
  * `controllers/game_controller.py`: Faz a ponte de ligação entre a UI e o modelo. Lida com a gravação/leitura de JSON e a IA.
  * `views/`: Telas e widgets construídos puramente em Python aproveitando as classes do KivyMD.
  
  * `cores.py`: Paleta de cores para as peças dos jogadores.

---

## 🌌 Próximos passos

* Implementar novos jogos e documentar como a interface reage a eles, buscando independência.
* Melhorar interfaces do aplicativo, a fim de deixá-las mais cativamtes, principalmente a de menu.
* Revisar código buscando possíveis redundâncias ou melhorias.

