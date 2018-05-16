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


