Projeto 2
Grupo ad007
Alunos nº 50006, 50013, 50019

As funcionalidades foram implementadas de acordo com a especificação do enunciado do projeto 2.

Os melhoramentos do projeto 1 para o projeto 2, para além do que foi proposto no projeto 2, nomeadamente multiplos clientes e estrutura RPC, são os seguintes:

- Correção de um bug que havia no STATS-Y após o tempo de requisição ter passado e o recurso ter-se tornado indisponível.
- A validação de mensagens do cliente passa para o lado do cliente.
- Verificação de erros do lado do cliente.

Algo relevante de mencionar será a limitação de saída do servidor, que por não estar no enunciado considera-se uma funcionalidade extra. 

Quando se executa o servidor, há um listener de stdin que escuta por uma mensagem 'exit'.
Devido à natureza de um threading TCP server, o servidor só irá realmente fechar quando todos os clientes se desliguem. Portanto não é imediatamente após a mensagem.

Também devido ao select a um sys.stdin, este não funciona no Windows.

