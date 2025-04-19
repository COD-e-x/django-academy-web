## Django Projects (Фреймворки)

### Сайт проекта, сервер настроен вручную:

  - > Реализованы базовые настройки безопасности, доступ по SSH, установлен и сконфигурирован Nginx.
    > Приложение запускается c Docker Compose (4 изолированных контейнера), подключён SSL-сертификат Let's Encrypt.
    > Для оптимизации и кеширования добавлен полноценный Redis, интегрированный с Django.

  - > Ссылка на сайт проекта: [https://www.cod-ex.ru](https://cod-ex.ru)

### FBV (завершено)
- Ссылка на проект: [django-learning-fbv](https://github.com/COD-e-x/django-learning-fbv)

### СBV

- Homework completed for module 16/7:
  - Заменил в модели (users) все функциональные представления (FBV) на классы (CBV)

- Homework completed for module 16/8:
  - Перевёл все представления dogs на классы (CBV)
  - Обновил валидаторы в приложение dogs
  - Настроил отображение родословной через formset
  - Добавил LoginRequiredMixin, HtmxRedirectMixin и IsOwnerOrAdminRequiredMixin для контроля доступа
  - Подключил favicon
  - Добавил core.signals.py

- Homework completed for module 16/9:
  - Redis
    - Настроил подключение Redis через .env
    - Добавил CacheService в services.py для централизованной работы с кешем
  - Перевёл DogsByBreed и BreedList на CBV, поправил кеширование
  - Добавил поле is_active в модель Dog
  - Обновил DogListView, добавил DogDeactivatedListView для управления активными/неактивными собаками
  - Добавил management-команду ccsu для создания БД PostgreSQL и пользователя из .env
  - Расширил ccsu команду добавлением ролей moderator и user
  - Удалил фикстуру user, обновил фикстуру dogs с привязкой к пользователям из команды
  - Добавил иконку входа в админку для администратора
  - ДобавДобавил docstrings в модуль dogsил

- Адаптировал приложение под мобильную версию (CSS + JS)
