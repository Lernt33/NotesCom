# admin/admin.py
import os
import sqlite3
from flask import Blueprint, render_template, request, redirect, url_for, flash, session



admin = Blueprint('admin', __name__,template_folder='templates',static_folder='static',)

@admin.route('/',methods=['GET'])
def adminpanel():
    # print('PRINTING FUNCTION',get_all_notes())
    return render_template('admin.html',notes=get_all_notes())


def get_all_notes():
    try:
        with sqlite3.connect('db.db') as conn:
            cur = conn.cursor()
            cur.execute(f'SELECT notes.*,users.email FROM users JOIN notes ON users.id = notes.id')
            result = cur.fetchall()
        return result
    except Exception as e:
        # print('Except : ',e)
        return "no"
