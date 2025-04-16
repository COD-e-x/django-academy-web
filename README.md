## Django Projects (Фреймворки)

### Сайт проекта, сервер настроен вручную:

  - > Реализованы базовые настройки безопасности, доступ по SSH, установлен и сконфигурирован
    > Nginx. Приложение запускается в Docker (3 изолированных контейнера), подключён SSL-сертификат Let's Encrypt.

  - > Ссылка на сайт проекта: [https://www.cod-ex.ru](https://cod-ex.ru)

### FBV (завершено)
- Ссылка на проект: [django-learning-fbv](https://github.com/COD-e-x/django-learning-fbv)

### СBV

| Commit                               | Описание              |
|--------------------------------------|-----------------------|
| Homework completed for module 16/7   | Ветка - homework-16-7 |


- Homework completed for module 16/7
  - Заменил в модели (users) все функциональные представления (FBV) на классы (CBV)

- Homework completed for module 16/8
  - Перевёл все представления dogs на классы (CBV)
  - Обновил валидаторы в приложение dogs
  - Настроил отображение родословной через formset
  - Добавил LoginRequiredMixin, HtmxRedirectMixin и IsOwnerOrAdminRequiredMixin для контроля доступа
  - Подключил favicon
  - Добавил core.signals.py

- Homework completed for module 16/9 