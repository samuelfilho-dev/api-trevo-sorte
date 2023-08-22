

# Inicia os serviços definidos no docker-compose.yml
docker-compose up

# Executa os comandos após os serviços estarem em execução
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser

# Mantém o container em execução para manter os serviços ativos
tail -f /dev/null
