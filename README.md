# weekendBrief

###### Телеграмм бот для распределения заявок с брифов

## Задача 
Написание телеграмм бота, который будет в удобной форме распределять и отображать информацию с брифов

### Брифы
Должен подхватывать евенты от заранее зарегестрированных доменов в базе, иметь дополняемую базу доменов.

### Заявки из брифов

Принимаются и записываются параллельно в систему. Являются json-объектами, передаваемыми через AJAJ. В боте имеют функциональную кнопку: отметить отвеченной.

### Контент
Имеет меню, состоящее из сайтов с брифами и парочку настроек, в виде консольных комманд.

При выборе сайта в меню клиент может просмотреть заявки из категорий: просмотренные, непросмотренные, отвеченные

Контент в заявках должен быть удобоваримо читаемым.

### Новые заявки
О каждой новой заявке должны приходить оповещения, оповещения должны быть короткими и понятными.

Вид оповещения: `Новая заявка на сайте: {name}`

### Дополнительные команды

Должна быть возможность добавления новых сайтов с брифами, форма подачи в которых возможно отличается от старых брифов.

Вид команды:  `/add {name} {domen} {password}`.

Удаление сайта из базы.

Вид команды:  `/remove {name}`.

Авторизация в сервисе

Вид команды:  `/auth {name} {password}`.

## Стек для разработки
* ### За базу данных отвечает ponyORM postgresql;
* ### Бот написан на библиотеке aiogram;
* ### Имеет айдентику реализованную через pydantic;
* ### Деплоится на сервер в Docker контейнер.
