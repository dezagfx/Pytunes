# Pytunes
Python Media Player Project - Client Version

O objectivo do presente trabalho, trata-se do desenvolvimento de duas aplicações numa arquitectura cliente-servidor,
que funcionem de forma interligada.
Por um lado o cliente trata-se de uma aplicação gráfica desenvolvida com recurso à biblioteca pyQt, que interage com a aplicação servidor, e possibilita ao utilizador aceder e escutar um repositório remoto de ficheiros mp3, bem como criar playlists com esses ficheiros.
Por outro lado temos a aplicação servidor que centraliza a base de dados e ficheiros mp3 e efectua streaming dos mesmos para o cliente.

Servidor

No caso da aplicação servidor optámos por utilizar uma web-framework escrita em python, que funciona sobre HTTP, denominada bottlepy (http://bottlepy.org/). A framework actua como um roteador, chamando diferentes métodos/funções consoante a URL solicitada pela aplicação cliente. Disponibiliza ainda ferramentas práticas para acesso às variáveis presentes no corpo do pedido http (parâmetros “GET”, “POST”), bem como um método fácil de servir ficheiros estáticos o qual utilizamos para fazer a componente do stream de mp3 para o cliente. Para a interacção com a base de dados optámos pela biblioteca SqlAlchemy (não utilizando as funcionalidades “ORM” da mesma, mas apenas a “Sql Expression Language”).

De forma a facilitar a validação da sessão do utilizador criámos um decorador, recorrendo ao módulo de python functools. Este decorador “envolve” as funções chamadas pela framework bottle aquando de um determinado pedido(que carece de autenticação) e verifica a presença e validade do token de sessão(como parametro GET ou POST) no pedido do cliente.

As passwords dos utilizadores são armazenadas na base de dados “hasheadas” com algoritmo bcrypt.

De forma a tornar a aplicação mais segura utilizamos o protocolo HTTPS - Secure Sockets Layer (SLL). Os certificados utilizados são auto-assinados, o que significa que não podem ser validados do lado da aplicação cliente(sendo no entanto a comunicação segura). Para gerarmos os certificados recorremos à ferramenta OpenSSL.

As rotas HTTP/ métodos expostos pela aplicação são os seguintes:

- /auth/login:

Parametros: nome de utilizador e password

Autentica o utilizador , armazena o token de sessão e devolve-o

- /auth/logout

Parametros: token de sessão

Apaga a sessão de utilizador da base de dados

- /auth/check_token - Parametros: token de sessão

Verifica se o token enviado existe na base de dados

- /auth/create_account - Parametros: nome de utilizador, palavra passe, confirmação de palvra passe, email

Cria uma nova conta de utilizador

/user/playlists – Parametros: token de sessão

Devolve todas as playlists(sem músicas) de um dado utilizador (correspondente ao token de sessão)

/playlists/<id> - Parametros: token de sessão, <id> corresponde ao id da playlist em questão

Devolve todas as músicas da playlist

/playlists/delete – Parametros: token de sessão, id da playlist

Elimina uma playlist da base de dados

/playlists/add – Parametros: token de sessão, nome da playlist

Adiciona uma playlist à base de dados

/playlists/<playlist_id>/add_music - Parametros: token de sessão, <playlist_id> corresponde à playlist em questão

Adiciona uma música à playlist

/musics/ - Parametros: token de sessão

Devolve todas as músicas do repositório

Base de Dados

De forma a podermos persistir os dados da aplicação foi necessária a criação de uma base de dados. Optamos por utilizar o SGBDR MySql para a base de dados e desenvolvemos a mesma com recurso ao software MySqlWorkbench.

Cliente

Em paralelo à criação da aplicação servidor criou-se uma aplicação gráfica baseada em Qt5, utilizando para tal a biblioteca PyQt que actua como binding entre o código escrito em python e a framwork subjacente escrita em C++.

Esta aplicação permite ao utilizador criar uma conta de utilizador, aceder a um repositório de música, criar playlists e adicionar músicas do repositório às playlists préviamente criadas.

De forma a poder comunicar com o servidor recorremos à biblioteca “requests”, que permite facilmente efectuar pedidos sobre HTTP/S e processar a resposta proveniente do servidor.

A nível da autenticação a aplicação cliente efectua um pedido à rota /auth/login, enviando o nome de utilizador e a password, caso o pedido seja validado, a resposta do servidor é um token de sessão que é armazenado recorrendo à classe QSettings, antes de ser armazenado o token de sessão é encriptado através do algorítmo AES – utilizando o módulo de python nativo Crypto.Cipher. Assim que o token de sessão se encontra armazenado, e até o utilizador terminar a sessão, a aplicação faz login automático e passa imediatamente para o écran inicial.

Todos os pedidos subsequentes ao servidor (após autenticação) incluem o token de sessão que identifica o utilizador da aplicação cliente do lado do servidor.

Para o streaming de música recorremos à biblioteca gstreamer ( nativa em algumas distribuições linux), e às bindings da mesma para python presentes no módulo gi.

Para o stream da música não efectuamos autenticação ( o que possibilita que esta possa ser reproduzida num outro cliente como por exemplo o itunes ou winamp), no entanto seria relativamente fácil de implementar esta funcionalidade, passando o token de sessão como parametro GET associado à URL do ficheiro remoto (por exemplo https://127.0.0.1:8080/musics/1.mp3?token=abcde)
