api sensores: \
GET /sensor-data:  
verifica se tem registro em cache, caso tenha, retorna o seu conteúdo \
caso esteja vazio ele gera dados randomicos de temperatura, pressão e tempo. \
adiciona esse novo registro ao redis e retorna o json do data. 

POST /alert: \
Obtem o body da requisição + o timestamp para cliar um json com essas infos. \
apos isso pega a url da api de python  e utilizando o post do axios, faz uma requisição para ela com o json de AlertData. 

api de eventos: \
POST /event : \
recebe a request da api de sensores \
adiciona o evento em uma lista do proprio python \
adiciona em chache redis \
retorna a mensagem falando que o evento foi recebido 

GET /events: \
verifica se tem em cache os eventos, senão retorna a propria lista do python em forma de json 

Api de logistica: \
GET /equipments: \
retorna os dados mocados dos equipamentos 

POST /dispatch: \
pega o conteudo da da requisição com file_get_contents \
pega o host do rabbitmq \
adiciona a a requisição a fila \
retorna o status da requisição 

Como estamos utilizando docker-compose utiliza-se o comando "docker-compose --build" e será automaticamente executado através dos dockerfiles em cada api