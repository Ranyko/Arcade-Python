class Textos:
    """
    Classe utilitária que centraliza todas as strings da interface do usuário.
    Garante que não existam textos 'hardcoded' nos arquivos de visão.
    """
    # Menu Screen
    TITULO_MENU = "Arcade Python!"
    SUBTITULO_MENU = "clássicos de tabuleiro"
    BTN_NOVA_PARTIDA = "Nova Partida"
    BTN_CARREGAR_PARTIDA = "Carregar Partida"
    BTN_SAIR = "Sair do Jogo"

    # Game Select Screen
    BTN_JOGAR = "Jogar"

    # Config Screen
    CHECK_IA = "Jogar contra Computador (IA)"
    LBL_JOGADOR_1 = "Jogador 1"
    HINT_JOGADOR_1 = "Nome do Jogador 1"
    LBL_JOGADOR_2 = "Jogador 2"
    HINT_JOGADOR_2 = "Nome do Jogador 2"
    HINT_COR = "Toque na cor para alterar"
    BTN_INICIAR = "Iniciar Partida"
    NOME_IA = "Computador (IA)"
    BTN_OK = "OK"
    ERRO_NOMES_VAZIOS = "Preencha os dois nomes!"
    ERRO_NOMES_IGUAIS = "Os nomes dos jogadores devem ser diferentes!"

    # Board Screen
    ESPACO_VAZIO = " "
    VEZ_DE_INICIAL = "Vez de: ..."
    VEZ_DE_FORMAT = "Vez de: {}"
    TEMPO_INICIAL = "15s"
    TEMPO_FORMAT = "{}s"
    PLACAR_INICIAL = "Placar: J1 0 x 0 J2"
    PLACAR_FORMAT = "Sessão: {} {} x {} {} (Empates: {})"
    BTN_VOLTAR_SALVAR = "Voltar ao Menu (Salvar)"
    MSG_SALVO = "Partida salva automaticamente!"
    MSG_TEMPO_ESGOTADO = "Tempo esgotado! Vez passada."
    IA_PENSANDO = "Computador pensando..."
    TITULO_VELHA = "Jogo da Velha"
    TITULO_CONNECT4 = "Connect 4"

    # Result Screen
    RESULTADO_VENCEU = "Jogador venceu!"
    PLACAR_ZERADO = "Placar: 0 x 0"
    BTN_NOVA_PARTIDA_RESULT = "Nova Partida"
    BTN_MENU_RESULT = "Voltar ao Menu"
