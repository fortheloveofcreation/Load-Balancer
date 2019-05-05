#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3

conn = sqlite3.connect("/opt/db/selfieless.db")
c = conn.cursor()
c.execute('PRAGMA foreign_keys = ON')
c.execute('''CREATE TABLE users(
    usr_name TEXT PRIMARY KEY NOT NULL,
    password TEXT NOT NULL);''')

c.execute('''CREATE TABLE categories(
    category_name TEXT PRIMARY KEY NOT NULL,
    acts INTEGER );''')

c.execute('''CREATE TABLE acts(
    act_id INTEGER PRIMARY KEY,
    user_name TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    caption TEXT NOT NULL,
    category TEXT NOT NULL,
    imgB64 TEXT NOT NULL,
    upvotes INTEGER,
    FOREIGN KEY (category) REFERENCES categories (category_name),
    FOREIGN KEY (user_name) REFERENCES users (usr_name));''')

conn.commit()
conn.close()


