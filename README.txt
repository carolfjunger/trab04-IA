Numa primeira tentativa, criamos uma máquina de estados para tratar os casos possíveis do mapa, como  "blocked", "breeze", "atacar", "fugir", "flash", "achou_ouro",
"achou_powerUp". entre outros comandos básicos, com uma movimentação trabalhando com aleatoriedade e sequências determinadas pra diferentes casos. Numa segunda adição, trabalhamos com um código A* para caminhar na parte do mapa já descoberta, 
mas este não possuía o devido tratamento dos casos como pegar tesouros, então para a competição mantivemos somente a lógica 
da máquina de estados. Contudo, criamos uma adaptação para juntar o A* com a lógica de movimentação e a máquina de estados cuidando da lógica de coleta, fuga e combate, mas faltaram casos para tornar esta versão mais estável.
