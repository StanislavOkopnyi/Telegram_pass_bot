# Телеграм бот - менеджер паролей

Для запуска бота необходимо будет клонировать репозиторий при помощи команды:

`git clone https://github.com/StanislavOkopnyi/Telegram_pass_bot.git`

Затем переходим в директорию с ботом:

`cd Telegram_pass_bot`

Для запуска бота вводим команду:

`make bot-token run-bot`

После ввода команд программа потребует ввести токен бота:

`Введите токен бота: `

После ввода токена бот начнет обрабатывать сообщения.

## Работа с ботом
#### После команды старт бот выведет приветственное сообщение и предложит пройти регистрацию:
![](https://github.com/StanislavOkopnyi/telegram_pass_bot_images/blob/main/Hi_message.png)
#### Если вы не хотите придумывать пароль для бота, имеется возможность его сгенерировать:
![](https://github.com/StanislavOkopnyi/telegram_pass_bot_images/blob/main/Registration.png)
![](https://github.com/StanislavOkopnyi/telegram_pass_bot_images/blob/main/registration_pass_gen.png)
#### После регистрации в боте появится возможность авторизоваться:
![](https://github.com/StanislavOkopnyi/telegram_pass_bot_images/blob/main/sign_in.png)
#### Авторизированный пользователь может сохранить пароль:
![](https://github.com/StanislavOkopnyi/telegram_pass_bot_images/blob/main/Password_saving.png)
#### Получить пароль/пароли к определенному сервису и ко всем сервисам:
![](https://github.com/StanislavOkopnyi/telegram_pass_bot_images/blob/main/get_one_password.png)
![](https://github.com/StanislavOkopnyi/telegram_pass_bot_images/blob/main/get_all_pass.png)
#### Удалить один/несколько паролей:
![](https://github.com/StanislavOkopnyi/telegram_pass_bot_images/blob/main/one_pass_delete.png)
![](https://github.com/StanislavOkopnyi/telegram_pass_bot_images/blob/main/delete_all_pass.png)
#### Выход из прошлых сценариев, если пользователь передумал:
![](https://github.com/StanislavOkopnyi/telegram_pass_bot_images/blob/main/stop.png)
#### Команда  `/help`  :
![](https://github.com/StanislavOkopnyi/telegram_pass_bot_images/blob/main/help.png)
#### Окончание сессии:
![](https://github.com/StanislavOkopnyi/telegram_pass_bot_images/blob/main/sign_out.png)


## Устройство бота
Данные о зарегистрированных пользователях хранятся в файле `pass.db`, что создается в той же директории из которой была запущена программа. 

Бот использует СУБД - **sqlite3**.

Пароль от аккаунта в боте не хранится в открытом виде - хранится кэш пароля.

Состояние сессии хранится фреймворком во время работы бота. При его отключении данные не сохраняются.
