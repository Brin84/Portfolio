1. Создал папку в поисковике с названием Portfolio
2. Создал новый репозиторий в GitHub
3. Настроил соединение локального проекта portfolio с удаленным проектом в GitHub c
   помощью следующих команд:
   1. git init - для инициализации пакета portfolio.
   2. git add remote origin "ссылка на проект в GitHub"
   3. git add . - добавил все файлы
   4. git commit -m "коммент" - закомитил все файлы
   5. git push origin master - запушил все файлы в ветку master

4. Создал файл .gitignore, записал туда файлы .idea/ и venv
5. Создал проект с фреймворком Django с помощью команды:
   django-admin startproject portfolio_app .
6. После запуска проекта появился пакет portfolio_app