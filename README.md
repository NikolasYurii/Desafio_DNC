# Desafio_DNC

# Zebrinha Azul - Sistema de Análise de Clima e Tráfego
## Descrição
A Zebrinha Azul é uma aplicação web para análise de dados de clima e tráfego. O sistema integra dados de várias fontes, processa e analisa esses dados, e fornece visualizações interativas para os usuários.

# Configuração
Configure as chaves da API:

Obtenha uma chave da API do OpenWeatherMap e atualize o arquivo config.py com a chave.</br>
Obtenha uma chave da API do Google Maps e atualize o arquivo config.py com a chave.</br>
Configure a conexão com o banco de dados:</br>

Atualize a string de conexão do PostgreSQL em config.py com as informações do seu banco de dados.
# Uso
Execute o script etl.py para extrair, transformar e carregar os dados de clima e tráfego no banco de dados:</br>
python etl.py</br>

Inicie o servidor da aplicação web executando o script app.py:</br>
python app.py</br>

Acesse a aplicação em seu navegador web:</br>
http://127.0.0.1:8050/

# Contribuição
Se você encontrar bugs ou problemas, abra uma issue no GitHub.</br>
Se deseja contribuir com código, faça um fork do repositório, faça suas alterações e envie um pull request.</br>
