# Trab04-IA

Numa primeira tentativa, criamos uma máquina de estados para tratar os casos possíveis do mapa: 
### blocked
Quando encontrar um obstáculo, ele fica girando para o mesmo lado e tentando sair enquanto estiver com o obstáculo

### breeze
Vemos qual foi a ação que o levou (andar ou andar_ré) e ele executa a oposta para não cair no buraco

### atacar
Quando vê o inimigo e tem mais de 50 de energia atira 

### fugir
Se vê o inimigo ou toma dano, faz um manhatan para fugir da linha de tiro

### flash
Tem o mesmo comportamento do breeze

### achou_ouro e achou_powerUp
Pega o item
 
## A*

Numa segunda adição, trabalhamos com um código A* para caminhar na parte do mapa já descoberta, 
mas este não possuía o devido tratamento dos casos como pegar tesouros, então para a competição mantivemos somente a lógica 
da máquina de estados. Contudo, criamos uma adaptação para juntar o A* com a lógica de movimentação e a máquina de estados cuidando da lógica de coleta, fuga e combate, mas faltaram casos para tornar esta versão mais estável.
