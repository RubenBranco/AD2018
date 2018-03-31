Projeto 2
Grupo ad007
Alunos nº 50006, 50013, 50019

As funcionalidades foram implementadas de acordo com a especificação do enunciado do projeto 2.

Algo relevante de mencionar será a limitação de saída do servidor. Quando se executa o servidor, há um listener de stdin que escuta por uma mensagem 'exit'.
Devido à natureza de um threading TCP server, o servidor só irá realmente fechar quando todos os clientes se desliguem. Portanto não é imediatamente após a mensagem.

