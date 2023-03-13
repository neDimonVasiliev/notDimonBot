# копируем файлы бота хост
scp -rp /home/dmitry/Yandex.Disk/Courses/Telegram/notDimonBot/ dmitry@192.168.1.48:/home/dmitry/notDimonBot


# подключаемся к хосту
ssh dmitry@192.168.1.48


# на хосте выполняем
nano .env # нужно изменить DB_HOST=127.0.0.1 на DB_HOST=db

docker-compose up
# потом можно нажать CTRL+z, чтобы бот перешел в фоновый режим


# чтобы подключиться к БД на удаленном хосте с локального компа, выполняем:
psql -h 192.168.1.48 -p 5432 -U postgres_admin botdb


### Обратный процесс ###
docker-compose down

# удаляем директорию
sudo rm -r -f notDimonBot

# можно почистить volumes и networks docker
