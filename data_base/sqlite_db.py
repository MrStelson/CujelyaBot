import sqlite3 as sq
from datetime import datetime, timedelta, timezone
import config
from logger.logger_users import logger_user_start

HOUR_OFFSET = config.HOUR_OFFSET
YEAR = config.YEAR


def sql_start():
    global base, cur
    base = sq.connect('cujelya_db')
    cur = base.cursor()
    if base:
        print('Data base connected OK!')
    base.execute('''
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            username VARCHAR (50),
            fullname VARCHAR (100),
            id_feedback INT,
            dateTimeFeedback DATETIME,
            status VARCHAR(20),
            chat_user_id INTEGER
        )
    ''')

    base.execute('''
        CREATE TABLE IF NOT EXISTS feedback(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            dateTimeFeedback DATETIME UNIQUE,
            status VARCHAR(20),
            user_id INT,
            username VARCHAR(50)            
        )
        ''')


async def get_date_time(date_time: str):
    date, time = date_time.split(" ")[0], date_time.split(" ")[1]
    date_day_month = f'{date.split("-")[2]}.{date.split("-")[1]}'
    time_hour_minute = f'{time.split(":")[0]}:{time.split(":")[1]}'
    date_time_dict = {
        'date': date_day_month,
        'time': time_hour_minute
    }
    return date_time_dict


async def sql_add_user(data_users):
    cur.execute('''
        INSERT OR IGNORE INTO users (user_id, username, fullName, id_feedback, dateTimeFeedback, status, chat_user_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', data_users)
    base.commit()


async def sql_add_feedback(data):
    data_values = tuple(data.values())
    month = int(data_values[0].split('.')[1])
    day = int(data_values[0].split('.')[0])
    hour = int(data_values[2].split(':')[0])
    minute = int(data_values[2].split(':')[1])
    date_time = datetime(year=YEAR,
                         month=month,
                         day=day,
                         hour=hour,
                         minute=minute)
    data_to_add = (date_time, data_values[3], data_values[4], data_values[5])
    cur.execute('''
        INSERT OR IGNORE INTO feedback (dateTimeFeedback, status, user_id, username)
        VALUES (?, ?, ?, ?)
    ''', data_to_add)
    base.commit()


async def sql_admin_show_all_feedbacks():
    data = cur.execute('SELECT * FROM feedback ORDER BY dateTimeFeedback')
    return data


async def sql_admin_show_booked_feedbacks():
    len_data = cur.execute('SELECT COUNT(*) FROM feedback WHERE status IN ("booked", "success")').fetchone()
    data = cur.execute('SELECT * FROM feedback WHERE status IN ("booked", "success") ORDER BY dateTimeFeedback')
    return data, len_data


async def sql_admin_delete_feedback(id_feedback=None):
    if cur.execute('SELECT id FROM feedback WHERE id=?', (id_feedback,)).fetchone():
        cur.execute('DELETE FROM feedback WHERE id=?', (id_feedback,))
        base.commit()
        cur.execute('''
            UPDATE users
            SET dateTimeFeedback=NULL,
                status="available"
            WHERE id_feedback=?
        ''', (id_feedback,))
        base.commit()


async def sql_admin_get_user(user_id):
    user = cur.execute('SELECT * from users WHERE user_id=?', (user_id,)).fetchone()
    return user


async def sql_admin_get_all_users_id():
    users_id = cur.execute('SELECT user_id from users').fetchall()
    return users_id


async def sql_admin_update_status(id_feedback=None, status=None):
    user_id = cur.execute('''
    SELECT user_id
    FROM feedback
    WHERE id=?
    ''', (id_feedback,)).fetchone()[0]
    if status == 'available':
        cur.execute('''
        UPDATE feedback 
        SET status=?,
            user_id=NULL,
            username=NULL
        WHERE id=?
        ''', (status, id_feedback))
        base.commit()

        cur.execute('''
        UPDATE users
        SET dateTimeFeedback=NULL,
            status="available"
        WHERE user_id=?
        ''', (user_id,))
        base.commit()
    else:
        cur.execute('UPDATE feedback SET status=? WHERE id=?', (status, id_feedback))
        base.commit()
    feedback = cur.execute(f'SELECT * FROM feedback WHERE id={id_feedback}').fetchone()
    return feedback


async def sql_admin_delete_passed_feedback():
    datetime_now = datetime.now() - timedelta(hours=HOUR_OFFSET)
    cur.execute('''
    DELETE FROM feedback
    WHERE dateTimeFeedback<?
    ''', (datetime_now,))
    base.commit()

    cur.execute('''
    UPDATE users
    SET dateTimeFeedback=NULL,
        status="available"
    WHERE dateTimeFeedback<?
    ''', (datetime_now,))
    base.commit()


async def sql_show_feedbacks():
    datetime_now = datetime.now() - timedelta(hours=HOUR_OFFSET)
    data = cur.execute('''
        SELECT *
        FROM feedback
        WHERE status="available" and dateTimeFeedback>?
        ORDER BY dateTimeFeedback
    ''', (datetime_now,)).fetchall()
    # dictionary of feedbacks
    data_dict = {}
    for entry in data:
        date_time = await get_date_time(entry[1])
        if date_time["date"] in data_dict:
            data_dict[date_time["date"]].append(date_time["time"])
        else:
            data_dict[date_time["date"]] = date_time["time"].split(" ")
    return data_dict


async def sql_check_user_status(user_id):
    user = cur.execute('SELECT * FROM users WHERE user_id=?', (user_id,)).fetchone()
    datetime_now = datetime.now() - timedelta(hours=HOUR_OFFSET)
    if user[4] is not None:
        date_time_user = await get_date_time(user[4])
        user_day = int(date_time_user['date'].split(".")[0])
        user_month = int(date_time_user['date'].split(".")[1])
        user_hour = int(date_time_user['time'].split(":")[0])
        user_minute = int(date_time_user['time'].split(":")[1])
        datetime_user = datetime(year=YEAR,
                                 day=user_day,
                                 month=user_month,
                                 hour=user_hour,
                                 minute=user_minute)
        if datetime_now >= datetime_user:
            cur.execute('''
            UPDATE users
            SET dateTimeFeedback=NULL,
                status="available"
            WHERE user_id=?
            ''', (user_id,))
            base.commit()
    return user


async def sql_get_feedback(date, time):
    date_time = datetime(year=YEAR,
                         month=int(date.split('.')[1]),
                         day=int(date.split('.')[0]),
                         hour=int(time.split(':')[0]),
                         minute=int(time.split(':')[1])
                         )
    feedback = cur.execute('SELECT * FROM feedback WHERE dateTimeFeedback=?', (date_time,)).fetchone()
    return feedback


async def sql_book_feedback(date, time, user_id):
    user = cur.execute('SELECT * from users WHERE user_id=?', (user_id,)).fetchone()
    date_time = datetime(year=YEAR,
                         month=int(date.split('.')[1]),
                         day=int(date.split('.')[0]),
                         hour=int(time.split(':')[0]),
                         minute=int(time.split(':')[1]))
    cur.execute('''
    UPDATE feedback
    SET status="booked",
        user_id=?,
        username=?
    WHERE dateTimeFeedback=?
    ''', (user_id, user[1], date_time))
    base.commit()

    id_feedback = cur.execute('''
        SELECT id
        FROM feedback
        WHERE dateTimeFeedback=?
    ''', (date_time,)).fetchone()

    cur.execute('''
    UPDATE users
    SET status="booked",
        id_feedback=?,
        dateTimeFeedback=?
    WHERE user_id=?
    ''', (id_feedback[0], date_time, user_id))
    base.commit()
