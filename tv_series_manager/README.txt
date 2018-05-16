Projeto 4
Grupo ad007
Alunos nº 50006, 50013, 50019

Do projeto 3 para o projeto 4 foi melhorado a geração de uma base de dados aquando o servidor arranca, enquanto que
no projeto 3 a geração da base de dados só era feita após o primeiro pedido desde o arranque, agora a geração
é feita imediatamente após o arranque.

NOTA IMPORTANTE: Para executar o servidor e cliente, o "working directory" deverá ser o diretório servidor e client,
respetivamente, isto devido à necessidade de encontrar os certificados para SSL/TLS, que estão em "../certs/*",
pelo que se o "working directory" não for uma desses diretórios, e for por exemplo, o diretório do projeto,
o diretório a cima já não terá certificados.

Nos comandos, devido à necessidade de desambiguação de certos parâmetros, foi necessário alterar a maneira com que 
os parâmetros são inseridos, as mudanças estão disponíveis através do comando HELP e estão listados a baixo:

(Nota às âspas)

ADD USER "NAME" "USERNAME" PASSWORD
ADD SERIE NAME YYYY-MM-DD "SYNOPSIS" CATEGORY_ID
ADD EPISODIO "NAME" "DESCRIPTION" SERIE_ID

* IPTABLES * 

Exemplos de operações

Pre-requisitos: 
Numa janela/pane de terminal: cd server/; python series_manager.py; (Arrancar servidor)
Noutra janela/pane de terminal: cd client/; python client.py; (Arrancar cliente)

Comandos na janela de cliente:

Funcionalidade: Adicionar utilizadores

ADD USER "Projeto AD" "projeto4" test123
    Resposta: Status Code: 201
              URI: /utilizadores/1

Funcionalidade: Adicionar serie

ADD SERIE Game of Thrones 2011-04-18 "Nine noble families fight for control over the mythical lands of Westeros, while an ancient enemy returns after being dormant for thousands of years." 1
    Resposta: Status Code: 201
              URI: /series/0

Funcionalidade: Adicionar episodio

ADD EPISODIO "Winter Is Coming" "Jon Arryn, the Hand of the King, is dead. King Robert Baratheon plans to ask his oldest friend, Eddard Stark, to take Jon's place. Across the sea, Viserys Targaryen plans to wed his sister to a nomadic warlord in exchange for an army." 0
    Resposta: Status code: 201
              URI: /episodios/0

Funcionalidade: Adicionar uma opinião de utilizador de uma serie

ADD 1 0 MB
    Resposta: Status Code: 201
              URI: /series/0

Funcionalidade: Mostrar um utilizador

SHOW USER 1
    Resposta: Status Code: 200
              Data: 1, Projeto AD, projeto4, test123

Funcionalidade: Mostrar TODOS os utilizadores:

SHOW ALL USERS
    Resposta: Status Code: 200
              Data: 0, rhbsda, rhbdfjsa, asdyuqwhu
              Data: 1, Projeto AD, projeto4, test123

Funcionalidade: Mostrar uma serie

SHOW SERIE 0
    Resposta: Status Code: 200
              Data: 0, Game of Thrones, 2011-04-18, Nine noble families fight for control over the mythical lands of Westeros, while an ancient enemy returns after being dormant for thousands of years., 1

Funcionalidade: Mostrar TODAS as series:

SHOW ALL SERIE
    Resposta: Status Code: 200
              Data: 0, Game of Thrones, 2011-04-18, Nine noble families fight for control over the mythical lands of Westeros, while an ancient enemy returns after being dormant for thousands of years., 1

Funcionalidade: Mostrar um episodio

SHOW EPISODIO 0
    Resposta: Status Code: 200
              Data: 0, Winter Is Coming, Jon Arryn, the Hand of the King, is dead. King Robert Baratheon plans to ask his oldest friend, Eddard Stark, to take Jon's place. Across the sea, Viserys Targaryen plans to wed his sister to a nomadic warlord in exchange for an army., 0

Funcionalidade: Mostrar TODOS os episodios

SHOW ALL EPISODIO
    Resposta: Status Code: 200
              Data: 0, Winter Is Coming, Jon Arryn, the Hand of the King, is dead. King Robert Baratheon plans to ask his oldest friend, Eddard Stark, to take Jon's place. Across the sea, Viserys Targaryen plans to wed his sister to a nomadic warlord in exchange for an army., 0

Funcionalidade: Mostar todas as series que um utilizador já deu opinião

SHOW ALL SERIE_U 0
    Resposta: Status Code: 200
              Data: 1, 5, 0

Funcionalidade: Mostrar todas as series de uma certa categoria

SHOW ALL SERIE_C 1
    Resposta: Status Code: 200
              Data: 0, Game of Thrones, 2011-04-18, Nine noble families fight for control over the mythical lands of Westeros, while an ancient enemy returns after being dormant for thousands of years., 1

Funcionalidade: Atualizar um utilizador

UPDATE USER 1 novapass
    Resposta: Status Code: 200
              Data: 1, Projeto AD, projeto4, novapass

Funcionalidade: Atualizar opinião de utilizador de uma serie

UPDATE SERIE 1 0 B
    Resposta: Status Code: 200
              Data: 1, 4, 0
