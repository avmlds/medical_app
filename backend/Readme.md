Применение миграций и создание миграций

1. Вносите изменения в ORM-модели, добавляете таблицы
2. В файле app.db.base импортируете все модели которые еще туда не были импортированы
3. Экспортируете переменную PYTHONPATH, находясь в папке `backend/app` выполняете `export PYTHONPATH=$(pwd)`
4. Запускаете команду  `alembic revision --autogenerate -m "НАЗВАНИЕ МИГРАЦИИ"`
5. Если alembic говорит что `FAILED: Target database is not up to date.`, то накатываем последние миграции через `alembic upgrade head`
6. Затем снова запускаете команду  `alembic revision --autogenerate -m "НАЗВАНИЕ МИГРАЦИИ"`
7. Применяете миграции к БД - `alembic upgrade head`

