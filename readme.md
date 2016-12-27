## Git-Automatizer, by Frobou
Se você:

 - leva trabalho pra casa 
 - trabalha com git 
 - faz push aqui e esquece de fazer pull ali

Seus problemas acabaram...
> O git-automatizer cuida de tudo pra mim, é o que dizem.

**É simples: adicione projetos na configuração da pasta e seja feliz.**

Cada automatizer-folder tem um arquivo de configuração que indica os repositórios a serem verificados. Voce chega de manhã no trabalho e roda um script...  
Adicionar um repositório é fácil:

    import getpass
    from git_automatizer.frobouConfig import FrobouConfig
    g = FrobouConfig()
    pwd = getpass.getpass('Password: ')
    g.add_project(repo='repo_name', service='github', protocol='https', username='username', ssh_key=False,
                  password=pwd, to_foler='destination')
    # g.remove_project('repo_name')
    # g.repo_list()
Algumas regras são:

 - repo e service são obrigatórios
 - repo é o nome do repositório remoto
 - service é o serviço, github e bitbucket, por enquanto...
 - protocol pode ser https ou ssh
 - username é o usuario do repositório remoto
 - ssh_key indica se vamos usar uma chave ssh
 - password é a senha do repositório remoto (codificada em base64, cuidado)
 - to_folder é a pasta do repositório local
 - se ssh_key for True, password deverá ser a chave ssh, protocol é alterado pra ssh
 - se password nao for informada e ssh_key for False, a senha é pedida no terminal
 - add_project também é usado para alterar um repositório
 - remove_project remove um repositório da configuração (não remove o repositório remoto)
 - repo_list lista os repositórios da configuração
 - repita o processo pra cada repositório que deseja controlar...
 
Isso cria um arquivo de configuração, fazendo a automatize-folder. Só isso.

***Agora é a hora legal.***

Se os repositórios nao existirem, precisamos clonar. Cada entrada na configuração será clonada. 

    from git_automatizer.frobouGit import FrobouGit
    fgit = FrobouGit()
    fgit.clone(True) # com instalacao dos componentes
    # ou
    fgit.clone() # sem instalacao dos componente

clone(True) faz coisas que clone() não faz.

 - se existir o arquivo composer.json ele roda composer install
 - se existir o arquivo package.json ele roda npm install
 - se existir o arquivo bower.json ele roda bower install

O relatório parece com isso:

Relatório final:  
Repositório frobou-db-connect clonado com sucesso  
Repositório outra_pasta clonado com sucesso  
Não consegui clonar o repositorio ApiTest. Ele já existe?  

Pronto, todos os repositórios estão ai (se as credenciais informadas estiverem corretas, claro), pode ver...

**E agora?**

    fgit.sync()
    
Qualquer repositório da configuração será sincronizado. O automatizer entra de pasta em pasta fazendo o pull, massssss

 - não faz nada se o repositório tiver alguma alteração
 - não faz a clonagem se o repositório não existir
 - não faz nada se o hash local for diferente do hash remoto
 - não faz nada se as credenciais nao conferirem

> Isso é bom, se tiver alterações na pasta eu esqueci de alguma coisa. Vou ter que fazer merge.

Esse é o propósito do projeto, rodar um sync antes começar o trabalho e outro antes de ir embora pra casa. Rodar um sync em casa antes e outro antes de dormir. Isso garante que o trabalho está sincronizado e não vou ter dores de cabeça.  
No final de cada processo temos um relatório assim:

Relatório final:  
Repositório outra_pasta já está sincronizado  
Destino ApiTest não existe  
Repositório frobou-db-connect já está sincronizado  

Bom, esse foi meu primeiro projeto sério em python, então o código não deve estar tão pythonico assim. Aceito sugestões e melhorias.  
Talvez tenha uma rotina para fazer o commit e pull, mas ainda tenho que pensar...  
Não coloquei no pypi, se o projeto amadurecer talvez. Por enquanto tem um arquivo de setup.  
Todos os testes feitos em python 2 e 3 funcionaram.  
Claro que devo ter esquecido de algo. Se lembrar eu atualizo.  
Bom uso.

