# Test Set

LOCK x y
TEST x y
STATS y
STATS-Y
STATS-N
RELEASE x y
TEST x y

Output esperado:
OK
LOCKED
1
1
N - 1
OK
UNLOCKED

## Iniciar servidor com n > 1 recursos e Y a 1

LOCK x y
LOCK x k

Output esperado:
OK
NOK

## Iniciar servidor com n > 1 recursos e K a 1

LOCK x y
RELEASE x y
LOCK x y

Output esperado:
OK
OK
NOK

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

## Inicio com N = 2

LOCK x y > 2

Output esperado:
UNKNOWN RESOURCE