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
  - Добавил Redis, класс CacheService в services.py для кеширования моделей breeds, dogs