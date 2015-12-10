#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unittest

from quikql import *


class QuikqlTest(unittest.TestCase):

    def setUp(self):
        testdb.create_table(tablename, schema)
        testdb.insert_rows(tablename, *entries)

    def tearDown(self):
        tables = testdb.get_tables()
        for table in tables:
            testdb.delete_table(table)

    def test_create_table(self):
        testtable = 'Open_Source_Software'
        schema = {'name':'TEXT', 'language':'TEXT', 'loc':'INTEGER'}
        testdb.create_table(testtable, schema)
        tables = [i[0] for i in testdb.get_tables()]
        self.assertIn(testtable, tables)

    def test_delete_table(self):
        testdb.delete_table(tablename)
        tables = testdb.get_tables()
        self.assertFalse(tables)

    def test_get_schema(self):
        test_schema = testdb.get_schema(tablename)
        schema_map = {i[1]:i[2] for i in test_schema}
        self.assertEqual(schema, schema_map)

    def test_get_tables(self):
        test_tables = testdb.get_tables()
        self.assertIn(tablename, test_tables[0])

    def test_insert_row(self):
        row = {'artist':'Lifetones', 'title':'Good Sides'}
        testdb.insert_row(tablename, row)

    def test_insert_rows(self):
        fields = ['duration', 'title', 'artist', 'track_number']
        rows = [{'artist':'damu', 'title':'How its suppose to be'},
                {'artist':'Nightmare on Wax', 'title':'You Wish'},
                {'artist':'Deep Space House', 'duration':12423},
                {'artist':'Bonobo', 'title':'Black sands', 'track_number':3}]
        testdb.insert_rows(tablename, *rows)
        table = testdb.dump_table(tablename)
        rows.extend(entries)
        current_entries = []
        for entry in table:
            row = {}
            for i in range(len(entry)):
                if entry[i] is not None:
                    row[fields[i]] = entry[i]
            if row:
                current_entries.append(row)
        for row in rows:
            print row
            self.assertIn(row, current_entries)

    def test_get_row(self):
        row = {'artist':'Lifetones', 'title':'Good Sides'}
        testdb.insert_row(tablename, row)
        testrow = testdb.get_row(tablename, row, size=ALL)
        retrieved_row = {'artist':testrow[0][2], 'title':testrow[0][1]}
        self.assertEqual(row, retrieved_row)

    def test_delete_row(self):
        row = {'artist':'Neal Howard', 'title':'The gathering'}
        row_retrieve = (None, u'The gathering', u'Neal Howard', None,)
        testdb.insert_row(tablename, row)
        table_before_del = testdb.dump_table(tablename)
        testdb.delete_row(tablename, row)
        table_after_del = testdb.dump_table(tablename)
        self.assertIn(row_retrieve, table_before_del)
        self.assertNotIn(row_retrieve, table_after_del)

    def test_retrieve_table_content(self):
        fields = [i[1] for i in testdb.get_schema('Music')]
        current_entries = [tuple(entry.get(field) for field in fields) 
                           for entry in entries]
        testtable = testdb.dump_table(tablename)
        self.assertEqual(testtable, current_entries)

    def test_insert_InvalidArg(self):
        invalid_row_insert = [('artist', 'Diplo')]
        self.assertRaises(InvalidArg, testdb.insert_row, 
                          tablename, invalid_row_insert)

    def test_delete_InvalidArg(self):
        invalid_row_delete = [('artist', 'Frank Sinatra')]
        self.assertRaises(InvalidArg, testdb.delete_row,
                          tablename, invalid_row_delete)

    def test_get_InvalidArg(self):
        invalid_row_get = [('artist', 'Franz Schubert')]
        self.assertRaises(InvalidArg, testdb.get_row,
                          tablename, invalid_row_get)
 
    def test_create_InvalidSQLType(self):
        table = 'Foo'
        schema = {'Bar':'Baz'}
        self.assertRaises(InvalidSQLType, testdb.create_table, table, schema)


if __name__ == '__main__':
    path = os.getcwd() + '/test.db'
    if os.path.isfile(path):
        os.unlink(path)
    testdb = Quikql(path)
    tablename = 'Music'
    schema = {'artist':'TEXT', 'title':'TEXT', 
              'duration':'INTEGER', 'track_number':'INTEGER'}
    entries = [{'artist':'Pryda', 'title':'opus', 'duration':532},
               {'artist':'Deadmau5', 'title':'everything after', 'track_number':3},
               {'artist':'Steve Angello', 'title':'voices', 'duration':531},
               {'artist':'Gramatik', 'title':'prophet2.0'},
               {'artist':'MF Doom', 'title':'Safed Musli'}]
    unittest.main(verbosity=3) 
