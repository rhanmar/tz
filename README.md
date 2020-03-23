	Установка

Перейти в диркеторию tz/job_task

Выполнить следующие команды:
docker-compose build
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose down

Переместить с заменой файлы из tz/right_versions в tz/job_task/deals

Раскомментировать строку в tz/job_task/job_task/urls.py:
# path('', include('deals.urls')),


	Запуск

docker-compose up


	Работа с сервисом

В браузере перейти на 127.0.0.1:8000 или 0.0.0.0:8000

Кнопка «Browse» необходима для выбора csv файла. Если формат файла не csv - появится уведомление о неправильном 
формате
Кнопка «Upload» необходима для загрузки и обработки файла
Кнопка «Get top customers» необходима для получения данных о пяти клиентах, потративших наибольшую сумму за весь
период

Если не отображается параметр "gems" у клиентов, необходимо перезагрузить приложение командой
docker-compose down
docker-compose up -d


	Прекращение работы с сервисом

docker-compose down -v
