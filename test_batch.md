Servidor:

## Inicializa corretamente com os parâmetros necessários

Código + output de servidor

## Mostra no ecrã informação sobre a ligação (IP e porta de origem) das conexões que aceita dos clientes

Ligar servidor e cliente e observar

## Verifica se existem recursos com bloqueios cujo tempo de concessão de exclusão mútua tenha expirado, e remove esses bloqueios nos recursos

python lock_server.py 9999 20 20 20 2
python lock_client.py 127.0.0.1 9999 1
> LOCK 1 2
Espera alguns segundos
> LOCK 1 5
Recurso 2 foi desbloqueado pois expiro o tempo

## Controla e gere os K bloqueios permitidos a um recurso, durante o funcionamento do gestor

python lock_server.py 9999 20 1 20 2
python lock_client.py 127.0.0.1 9999 1
LOCK 1 1
Esperar uns segundos 
LOCK 1 1

## Desativa o recurso, ficando indisponível a bloqueios, após o recurso ser bloqueado K vezes

python lock_server.py 9999 20 1 20 2
python lock_client.py 127.0.0.1 9999 1
LOCK 1 1
Esperar uns segundos 
LOCK 1 1

## Controla e gere os Y recursos bloqueados permitidos, num dado momento, durante o funcionamento do gestor

python lock_server.py 9999 20 20 1 100
python lock_client.py 127.0.0.1 9999 1
LOCK 1 1
LOCK 1 2
RELEASE 1 1
LOCK 1 2

## Não permite bloqueios a mais recursos quando o número de recursos bloqueados atinge Y

python lock_server.py 9999 20 20 1 100
python lock_client.py 127.0.0.1 9999 1
LOCK 1 1
LOCK 1 2
RELEASE 1 1
LOCK 1 2

## Output do estado dos recursos após processamento de um pedido

Fazer um pedido

Cliente:

## Teste de um recurso

python lock_server.py 9999 4 2 2 2
python lock_client.py 127.0.0.1 9999 1
LOCK 1 1
TEST 1
DISABLE

## Status de um recurso
python lock_server.py 9999 4 5 2 10
python lock_client.py 127.0.0.1 9999 1
LOCK 1 1
OK
LOCK 1 1
OK
STATS 1
2

## Liberta recurso
python lock_server.py 9999 4 10 2 50
python lock_client.py 127.0.0.1 9999 1
LOCK 1 1
OK
RELEASE 1 1
OK
