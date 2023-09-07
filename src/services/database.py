import mysql.connector
import random


class DatabaseManager:
    def __init__(self):
        # Initialization connection with DB
        self.db = mysql.connector.connect(
            user='root',
            password='hokkaido',
            host='localhost',
            port='3306',
            database='anonbot'
        )
        # Creating cursor for making queries
        self.cursor = self.db.cursor()

    # Method for entering the context
    def __enter__(self):
        return self.cursor

    # Method for exiting the context
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.commit()  # Commit changes
        self.cursor.close()
        self.db.close()


async def get_user(user_id):
    query = 'SELECT * FROM users WHERE user_id = %s'
    with DatabaseManager() as dbm_cursor:
        dbm_cursor.execute(query, (user_id,))
        return dbm_cursor.fetchone()


async def set_user(user_id):
    query = 'INSERT INTO users (user_id) VALUES (%s)'
    with DatabaseManager() as dbm_cursor:
        dbm_cursor.execute(query, (user_id,))


async def edit_sex(user_id, sex):
    query = 'UPDATE users SET sex = %s WHERE user_id = %s'
    with DatabaseManager() as dbm_cursor:
        dbm_cursor.execute(query, (sex, user_id))


async def find(user_id, user_sex):
    query = 'SELECT * FROM wait_list WHERE user_sex = %s AND user_id != %s'
    with DatabaseManager() as dbm_cursor:
        dbm_cursor.execute(query, (user_sex, user_id))
        data = dbm_cursor.fetchall()
    if data:
        # Choose random user from list
        partner_id = random.choice(data)[1]
        update_query1 = 'UPDATE users SET partner_id = %s WHERE user_id = %s'
        update_query2 = 'UPDATE users SET partner_id = %s WHERE user_id = %s'
        delete_query = 'DELETE FROM wait_list WHERE user_id = %s'
        with DatabaseManager() as dbm_cursor:
            dbm_cursor.execute(update_query1, (user_id, partner_id))
            dbm_cursor.execute(update_query2, (partner_id, user_id))
            dbm_cursor.execute(delete_query, (partner_id,))
            return partner_id
    else:
        # If there's no users, add this user to wait list
        user = await get_user(user_id)
        insert_query = 'INSERT INTO wait_list (user_id, user_sex) VALUES (%s, %s)'
        with DatabaseManager() as dbm_cursor:
            dbm_cursor.execute(insert_query, (user_id, user[2]))
        return None


async def find_sexless(user_id):
    query = 'SELECT * FROM wait_list WHERE user_id != %s'
    with DatabaseManager() as dbm_cursor:
        dbm_cursor.execute(query, (user_id,))
        data = dbm_cursor.fetchall()
    if data:
        # Choose random user from list
        partner_id = random.choice(data)[1]
        update_query1 = 'UPDATE users SET partner_id = %s WHERE user_id = %s'
        update_query2 = 'UPDATE users SET partner_id = %s WHERE user_id = %s'
        delete_query = 'DELETE FROM wait_list WHERE user_id = %s'
        with DatabaseManager() as dbm_cursor:
            dbm_cursor.execute(update_query1, (user_id, partner_id))
            dbm_cursor.execute(update_query2, (partner_id, user_id))
            dbm_cursor.execute(delete_query, (partner_id,))
            return partner_id
    else:
        # If there's no users, add this user to wait list
        user = await get_user(user_id)
        insert_query = 'INSERT INTO wait_list (user_id, user_sex) VALUES (%s, %s)'
        with DatabaseManager() as dbm_cursor:
            dbm_cursor.execute(insert_query, (user_id, user[2]))
        return None


async def set_message(user_id, msg):
    query = 'UPDATE users SET message = %s WHERE user_id = %s'
    with DatabaseManager() as dbm_cursor:
        dbm_cursor.execute(query, (msg, user_id))


# Function for stop dialog
async def stop_dialog(user_id):
    update_query = 'UPDATE users SET partner_id = %s WHERE user_id = %s'
    with DatabaseManager() as dbm_cursor:
        dbm_cursor.execute(update_query, ("None", user_id))
        user = await get_user(user_id)
        dbm_cursor.execute(update_query, ("None", user[3]))
        return user[3]


# Function for stop searching partner
async def stop_find(user_id):
    query = 'DELETE FROM wait_list WHERE user_id = %s'
    with DatabaseManager() as dbm_cursor:
        dbm_cursor.execute(query, (user_id,))
