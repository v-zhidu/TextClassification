# !-*- encoding=utf-8 -*-
"""
    nlp.azure_table.py
    ~~~~~~~~~~~~~~~~~~

    A brief description goes here.

    : copyright: (c) YEAR by v-zhidu.
    : license: LICENSE_NAME, see LICENSE_FILE
"""
from azure.storage.table import TableService, Entity

table_service = TableService(
    account_name='raven',
    account_key='nL4Z4ick3pai0y/vpcUKIHr/4VN95xplw94BCFCsqtGTvrX7KoK0kDjobmk3X+WyHZ0o+lyo6NmpHcTW1fJxSw==')

table_service.create_table('t_news')
