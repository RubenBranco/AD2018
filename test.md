# Test Set

## Teste geral de comandos

LOCK x y
TEST y
STATS y
STATS-Y
STATS-N
RELEASE x y
TEST y

Output esperado:
OK
LOCKED
1
1
N - 1
OK
UNLOCKED

Output real: Tudo como esperado

## Iniciar servidor com n > 1 recursos e Y a 1

LOCK x y
LOCK x k

Output esperado:
OK
NOK

Output real: Tudo como esperado

## Iniciar servidor com n > 1 recursos e K a 1

LOCK x y
RELEASE x y
LOCK x y

Output esperado:
OK
OK
NOK

Output real: Tudo como esperado

## Inicio arbitrário

LOCK x y
RELEASE k y

Output esperado:
OK
NOK

LOCK x y
LOCK k y

Output esperado:
OK
NOK

Output real: Tudo como esperado em ambos

## Inicio com N = 2

LOCK x y > 2

Output esperado:
UNKNOWN RESOURCE

Output real: Tudo como esperado em ambos