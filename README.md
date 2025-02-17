------Запуск приложения-------

1) docker compose up -d
2) docker exec -it app /bin/bash 
3) alembic upgrade head
4) exit

--------------tests-------------

1) docker compose -f tests/docker-compose.test.yaml up -d
2) pytest
