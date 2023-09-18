# CujelyaBot

## Information about Frameworks:
- aiogram
---
### Start project
```
python -m venv venv
```
```
venv\Scripts\activate
```
```
pip install -r requrements.txt
```
```
python app.py
```
---
## Telegram Bot for UI/UX artist Cujel (https://t.me/CujelyaBot)

### Functional for users:
- send questions for Cujel
- send file (resume) for Cujel
- sign up for a consultation

### Functional for admin:
- view active and all consultation
- add consultation with validation dateTime
- update consultation (delete, update status)
- send mailing for all users

---
#### Before start project necessary create config file "config.py" with cons:
- BOT_TOKEN = \<your token\>
- CHAT_ID = \<your chat id\> (for send message from users )
- ADMIN_ID_FIRST = \<admin id\> (for settings feedbacks and send mailing )
- HOUR_OFFSET = \<your hour offset\> (Default = 4)
- YEAR = \<your year\> (Default = 2023)
