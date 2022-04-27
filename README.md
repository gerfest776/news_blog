## <a name="guides"></a> Инструкции

## URL

* gerfest.site/swagger

### <a name="launch-app"></a> Запуск приложения
 
 * Docker Compose

Скопировать содержимое файла .test_env в .env

Находясь в папке с файлом `docker-compose.yml` выполнить в терминале:

	docker-compose up

### <a name="launch-app"></a> Запуск тестов

Находясь в папке с файлом `manage.py` выполнить в терминале:

	python manage.py test
  
  
  ## <a name="handlers"></a> Реализация REST API

### <a name="post-import"></a> Авторизация
В сервисе используются 2 вида авторизации: Basic Auth. И с помощью JWT токенов.


## POST /user/create 

В данном url реализован процесс регистрации пользователя. Пользователь может быть автором, либо подписчиком.

## Авторизация по JWT токенам

* POST /api/token/ - url  получения токена

* POST /api/token/refresh - url для обновления токена, если его время жизни истекло

Токен можно ввести в swagger. Пример: Bearer your_token








## POST /user/create/subscribe

Данный url позволяет подписчику подписаться на автора, для дальнейшей логики








## GET /api/news

url для свободного просмотра новых статей








## POST /api/news/create

url для создания статей, создавать их может только автор







## GET /api/news/subscriptions

url для пользователей, которые подписывались на авторов из url'a выше. Отображает сущности, тип которых false.







## PATCH | DELETE /api/news/{id}/edit

url для:

* изменения данных

* удаления данных


