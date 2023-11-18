import os

import openpyxl as openpyxl
import requests
# current script's directory
script_dir = os.path.dirname(os.path.realpath(__file__))
# absolute path to file
excel_file_path = os.path.join(script_dir, 'data.xlsx')
work_book = openpyxl.load_workbook(excel_file_path)


def get_create_post_data_from_excel():
    sheet = work_book['post_data']
    post_data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        post_dict = {
            'title': row[0],
            'body': row[1],
        }
        post_data.append(post_dict)
    return post_data
