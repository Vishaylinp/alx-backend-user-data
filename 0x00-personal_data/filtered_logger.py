#!/usr/bin/env python3
"""Personal data"""
from typing import List
import re
import logging
from os import environ
import mysql.connector


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """replace sensitive information with a redacted str"""

    for field in fields:
        message = re.sub(f"{field}=.*?{separator}",
                         f"{field}={redaction}{separator}", message)
    return message


def get_logger() -> logging.Logger:
    """returns a Logger object"""

    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logging.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """return a database"""

    username = environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    db_Host = environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DATA_DB_NAME")

    connect = mysql.connector.connection.MySQLConnection(user=username,
                                                         password=password,
                                                         host=db_Host,
                                                         database=db_name)
    return connect


def main():
    """obtain database connection"""
    db = get_db()
    db_cursor = db.cursor()
    db_cursor.execute("SELECT * FROM users;")
    fields_nm = [c[0] for c in db_cursor.description]

    logger = get_logger()

    for row in db_cursor:
        form_data = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, fields_nm))
        logger.info(form_data.strip())

    db_cursor.close()
    db.close()


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """initialisation"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log"""

        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


if __name__ == "__main__":
    main()
