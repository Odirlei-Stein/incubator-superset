# Como esta rodando?
Esta rodando usando gunicorn e systemd. Usei este tutorial https://docs.gunicorn.org/en/stable/deploy.html#systemd

# Onde esta configurado?
O systemd service esta configurado em `/etc/systemd/system/gunicorn.service` e `/etc/systemd/system/gunicorn.socket`.

O proxy reverso do nginx esta configurado em `/etc/nginx/sites-available/default`

O certbot do Lets encrypt esta configurado para o domínio.

O superset precisa de algumas variaveis de ambiente para funcionar. O systemd esta pegando estas variaveis de `local_app/environment`

# Como parar ou iniciar o serviço
O serviço inicia com o sistema, mas caso precise é só rodar
- `sudo service stop gunicorn`
- `sudo service start gunicorn`

# Como atualizar para a versão atual do superset
Pegue a ultima versao do branch chamado superset
- `git pull superset master`

Tudo deve se atualizar sozinho e fazer os merges necessários

# Como fiz a autenticação via JWT?

Verificar arquivo `local_app/security.py`

# Como faço filtrar os dados que trazem para o usuário?
Basicamente fazendo uma mutação na SQL que esta sendo executada. Verificar arquivo `local_app/mutator.py`

# Como mudo o front-end?
Alterar arquivos react e css em `superset/assets`

Rodar js em modo de dev `cd superset/assets && npm run dev`. Este comando vai dar watch nos arquivos e atualizar sozinho o build quando alguma mudança ocorrer.

Quando finalizar as alterações rodar a build de produção para melhorar o desempenho `cd superset/assets && npm run build`

# Foi modificado algo do backend?
Sim, poucas coisas. Verificar os commits que foram feitos.