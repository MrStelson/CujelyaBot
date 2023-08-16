from datetime import datetime


async def logger_user_start(data_users):
    datetime_now = datetime.now().strftime('%m-%d %H:%M:%S')
    with open('log_file.txt', 'r+') as log_file:
        log_file.seek(0, 2)
        log_file.write(f'\n{datetime_now}: {str(data_users)}')
