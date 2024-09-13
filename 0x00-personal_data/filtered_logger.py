#!/usr/bin/env python3
"""Regex-ing"""
from typing import List
import re
import logging
import mysql.connector
import os

PII_FIELDS = ("name", "email", "password", "ssn", "phone")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns regex obfuscated log messages"""
    pattern = rf'({"|".join(map(re.escape, fields))})=([^{separator}]*)'
    return re.sub(pattern, rf'\1={redaction}', message)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Returns filtered values from log records"""
        message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object"""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = RedactingFormatter(list(PII_FIELDS))
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Connection to MySQL environment"""
    return mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )


def main() -> None:
    """
    Obtain database connection using get_db,
    retrieve all rows in the users table and display
    each row under a filtered format
    """
    logger = get_logger()
    db = get_db()
    cursor = db.cursor()

    try:
        cursor.execute("SELECT * FROM users;")
        headers = [field[0] for field in cursor.description]
        for row in cursor:
            info_answer = '; '.join(
                    f'{header}={value}' for header, value in zip(
                        headers, row))
            logger.info(info_answer)
    except mysql.connector.Error as err:
        logger.error(f"Database error: {err}")
    finally:
        cursor.close()
        db.close()


if __name__ == '__main__':
    main()
