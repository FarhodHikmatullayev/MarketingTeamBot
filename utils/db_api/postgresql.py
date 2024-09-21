import datetime
from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config
from data.config import DEVELOPMENT_MODE


class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        print('DEVELOPMENT_MODE', DEVELOPMENT_MODE)
        if DEVELOPMENT_MODE:
            self.pool = await asyncpg.create_pool(
                user=config.DB_USER,
                password=config.DB_PASS,
                host=config.DB_HOST,
                database=config.DB_NAME
            )
        else:
            self.pool = await asyncpg.create_pool(
                dsn=config.DATABASE_URL
            )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    # for users
    async def create_user(self, phone, username, telegram_id, full_name):
        sql = "INSERT INTO Users (phone, username, telegram_id, full_name) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, phone, username, telegram_id, full_name, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users WHERE is_active = TRUE"
        return await self.execute(sql, fetch=True)

    async def select_users(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    # for warnings
    async def create_warning(self, user_id, text, warned_by_id, created_at=datetime.datetime.now()):
        sql = "INSERT INTO Warnings (user_id, text, warned_by_id, created_at) VALUES($1, $2, $3, $4) returning *"
        return await self.execute(sql, user_id, text, warned_by_id, created_at, fetchrow=True)

    async def select_warnings(self, **kwargs):
        sql = "SELECT * FROM Warnings WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_all_applications(self):
        sql = "SELECT * FROM Applications"
        return await self.execute(sql, fetch=True)

    async def select_applications(self, **kwargs):
        sql = "SELECT * FROM Applications WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    # for applications
    async def create_application(self, user_id, description, created_at=datetime.datetime.now(),
                                 is_confirmed=False, confirmed_at=None, confirmed_by_id=None):
        sql = "INSERT INTO Applications (user_id, description, created_at, is_confirmed, confirmed_at, confirmed_by_id) VALUES($1, $2, $3, $4, $5, $6) returning *"
        return await self.execute(sql, user_id, description, created_at, is_confirmed, confirmed_at, confirmed_by_id,
                                  fetchrow=True)

    async def update_application(self, id, confirmed_by_id, is_confirmed=False, confirmed_at=datetime.datetime.now()):
        sql = "UPDATE Applications SET confirmed_by_id=$2, is_confirmed=$3, confirmed_at=$4 WHERE id=$1"
        return await self.execute(sql, id, confirmed_by_id, is_confirmed, confirmed_at, execute=True)

    async def update_application_confirmed_description(self, id, confirmed_description):
        sql = "UPDATE Applications SET confirmed_description=$2 WHERE id=$1"
        return await self.execute(sql, id, confirmed_description, execute=True)

    # for status

    async def select_all_status(self):
        # sql = "SELECT * FROM Status"
        sql = """
                SELECT s.*
                FROM Status s
                INNER JOIN Users u ON s.user_id = u.id
                WHERE u.is_active = TRUE
            """
        return await self.execute(sql, fetch=True)

    async def create_status(self, user_id, at_work=False):
        sql = "INSERT INTO Status (user_id, at_work) VALUES($1, $2) returning *"
        return await self.execute(sql, user_id, at_work, fetchrow=True)

    async def select_status(self, **kwargs):
        sql = "SELECT * FROM Status WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def update_status(self, id, user_id, at_work=False):
        sql = "UPDATE Status SET user_id=$2, at_work=$3 WHERE id=$1"
        return await self.execute(sql, id, user_id, at_work, execute=True)

    # for registrations
    async def create_registration(self, user_id, arrival_time):
        sql = "INSERT INTO Registrations (user_id, arrival_time) VALUES($1, $2) returning *"
        return await self.execute(sql, user_id, arrival_time, fetchrow=True)

    async def update_registration(self, id, user_id, arrival_time, departure_time, total_time):
        sql = "UPDATE Registrations SET user_id=$2, arrival_time=$3, departure_time=$4, total_time=$5 WHERE id=$1"
        return await self.execute(sql, id, user_id, arrival_time, departure_time, total_time, execute=True)

    async def get_today_registrations_for_user_by_arrival_time(self, user_id):
        today = datetime.datetime.now().date()
        sql = """
            SELECT * FROM Registrations
            WHERE DATE(arrival_time) = $1 AND user_id = $2
        """
        return await self.execute(sql, today, user_id, fetch=True)

    async def get_today_registrations_for_user_by_departure_time(self, user_id):
        today = datetime.datetime.now().date()
        sql = """
            SELECT * FROM Registrations
            WHERE DATE(departure_time) = $1 AND user_id = $2
        """
        return await self.execute(sql, today, user_id, fetch=True)
