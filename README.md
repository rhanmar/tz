# Веб-сервис (тестовое задание)

## Установка

1. Перейти в диркеторию *tz/job_task* и выполнить следующие команды:
```
docker-compose build
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose down
```
2. Переместить с заменой файлы из *tz/right_versions* в *tz/job_task/deals*

3. Раскомментировать строку в *tz/job_task/job_task/urls.py*:
`# path('', include('deals.urls')),`


## Запуск

Для запуска веб-сервиса использовать команду:
`docker-compose up`


## Работа с сервисом

В браузере перейти на 127.0.0.1:8000 или 0.0.0.0:8000  
Описание интерфейса:
- Кнопка «Browse» необходима для выбора csv файла. Если формат файла не csv - появится уведомление о неправильном 
формате
- Кнопка «Upload» необходима для загрузки и обработки файла
- Кнопка «Get top customers» необходима для получения данных о пяти клиентах, потративших наибольшую сумму за весь
период

Если после загрузки в ответе у клиентов не отображается параметр "gems", необходимо перезагрузить приложение командами:
```
docker-compose down
docker-compose up -d
```


## Прекращение работы с сервисом

Для остановки сервиса использовать команду:
`docker-compose down -v`
