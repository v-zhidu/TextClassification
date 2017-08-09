# !-*- encoding=utf-8 -*-
"""
    nlp.azure_table.py
    ~~~~~~~~~~~~~~~~~~

    A brief description goes here.

    : copyright: (c) YEAR by v-zhidu.
    : license: LICENSE_NAME, see LICENSE_FILE
"""
from azure.storage.table import TableService, Entity


class AzureTable(object):
    def __init__(self):
        self._table_service = TableService(
            account_name='raven',
            account_key='nL4Z4ick3pai0y/vpcUKIHr/4VN95xplw94BCFCsqtGTvrX7KoK0kDjobmk3X+WyHZ0o+lyo6NmpHcTW1fJxSw==', endpoint_suffix='core.chinacloudapi.cn')

    def create_table(self, table_name):
        self._table_service.create_table(table_name)

    def insert_entities(self, table_name, entities):
        with self._table_service.batch(table_name) as batch:
            for item in entities:
                batch.insert_entity(item)
            self._table_service.commit_batch(table_name, batch)

    def insert_entity(self, table_name, entity):
        self._table_service.insert_entity(table_name, entity)


if __name__ == '__main__':
    a = AzureTable()
    a.insert_entity('news', {'PartitionKey': 'test',
                             'RowKey': '001', 'value': '2'})
