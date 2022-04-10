from __future__ import annotations

import csv
import json
import os

from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class ItmoTable:
    """
    Class for collecting grades of students of KTy2020 from several Google Sheets into one table.

    Used Google Sheets:
    https://docs.google.com/spreadsheets/d/1UxWfy2n2osxERr1GvkaYydHBOwMHEUqfjNuwD6RcDQc/
    https://docs.google.com/spreadsheets/d/1Cex024D28TNI63iUCU5ftU1WBgBnPrNWIiEDw_5TtFk/
    https://docs.google.com/spreadsheets/d/1UxWfy2n2osxERr1GvkaYydHBOwMHEUqfjNuwD6RcDQc/
    https://docs.google.com/spreadsheets/d/1X17zc7yRq7o4ge6KreFfQjbxR2B141-Ygx4nCdGeuxI/
    https://docs.google.com/spreadsheets/d/15pjGIzgfVkVJoXspghvrprrBvPCoJUQbOBA37Et2ChE/
    https://docs.google.com/spreadsheets/d/1F3hoDX6mmFtmBKRiV-iwfp99vetHae5SwB7E-RHrjbY/
    https://docs.google.com/spreadsheets/d/1g4P-QmUCiHH1i-nKb8LBjriSEfGK4mMQdr1h2W2x3n8/
    https://docs.google.com/spreadsheets/d/1YOTxFL4CZb0cDhueUFsXEJPa4bM0GMzHBkirJBGsCHw/
    https://docs.google.com/spreadsheets/d/13MvoS91pdRSZG9tck79PdNE46LT4KZzpiAymw4lf4Ys/
    """

    subject_pos = {
        'Java': 0,
        'ДМ': 1,
        'МатЛог': 2,
        'АиСД': 3,
        'МатАн': 4,
        'МетОпт': 5
    }
    """Subjects and their positions in table"""

    subjects_count = len(subject_pos)

    def __init__(self):
        """
        Initialization of Google Sheets API.

        Copied from here:
        https://developers.google.com/sheets/api/quickstart/python
        """
        _scopes = ['https://www.googleapis.com/auth/spreadsheets.readonly']
        _creds = None
        if os.path.exists('credentials/sheets-token.json'):
            _creds = Credentials.from_authorized_user_file('credentials/sheets-token.json', _scopes)
        if not _creds or not _creds.valid:
            if _creds and _creds.expired and _creds.refresh_token:
                _creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials/sheets-credentials.json', _scopes)
                _creds = flow.run_local_server(port=0)
            with open('credentials/sheets-token.json', 'w') as token:
                token.write(_creds.to_json())
        _service = build('sheets', 'v4', credentials=_creds)
        self._sheet = _service.spreadsheets()
        self._table = {}

    def __str__(self):
        s = ''
        for name, grades in self._table.items():
            s += f'{name.rjust(25)}: {grades}\n'
        return s

    def collect_all_subjects(self) -> ItmoTable:
        self._collect_discrete_math()
        self._collect_algorithms()
        self._collect_matlog()
        self._collect_java()
        self._collect_calculus()
        self._collect_optimization_methods()
        return self

    def sort(self) -> ItmoTable:
        """Sorts table by keys in lexicographical order and returns it."""

        self._table = dict(sorted(self._table.items()))
        return self

    def delete_dead_students(self, min_grades_sum: int = 0) -> ItmoTable:
        """Deletes from the table students that have less than required sum of grades."""

        for student, grades in self._table.copy().items():
            if sum(grades) < min_grades_sum:
                del self._table[student]
        return self

    def to_dict(self) -> dict:
        return self._table

    def to_json(self) -> str:
        return json.dumps(self._table, ensure_ascii=False)

    def to_csv(self) -> None:
        """Writes table to csv file"""

        directory = 'itmo-tables-samples'
        file = f'{get_formatted_time_for_file_name()}.csv'
        path = f'{directory}/{file}'
        with open(path, 'w', encoding='utf-8-sig', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow((get_time(), '', '', '', '', '', ''))
            writer.writerow(('Студент', *ItmoTable.subject_pos.keys()))
            for student, grades in self._table.items():
                writer.writerow((student, *grades))

    def _collect_matlog(self, subject='МатЛог') -> ItmoTable:
        # MatLog (all groups)
        self._add_to_table(subject=subject,
                           spread_sheet_id='1UxWfy2n2osxERr1GvkaYydHBOwMHEUqfjNuwD6RcDQc',
                           sheet_list='матлог',
                           names='A3:A133',
                           grades='E3:E133')

        self._add_to_table(subject=subject,
                           spread_sheet_id='13MvoS91pdRSZG9tck79PdNE46LT4KZzpiAymw4lf4Ys',
                           sheet_list='Баллы',
                           names='A2:A36',
                           grades='B2:B36')
        return self

    def _collect_algorithms(self, subject='АиСД') -> ItmoTable:
        # A&DS (34-37 groups)
        self._add_to_table(subject=subject,
                           spread_sheet_id='1Cex024D28TNI63iUCU5ftU1WBgBnPrNWIiEDw_5TtFk',
                           sheet_list='34-37',
                           names='B3:B120',
                           grades='G3:G120')

        # A&DS (38-39 groups)
        self._add_to_table(subject='АиСД',
                           spread_sheet_id='1UxWfy2n2osxERr1GvkaYydHBOwMHEUqfjNuwD6RcDQc',
                           sheet_list='4 семестр - Общая табличка',
                           names='C5:C31',
                           grades='P5:P31')
        return self

    def _collect_discrete_math(self, subject='ДМ') -> ItmoTable:
        # DM (all groups)
        self._add_to_table(subject=subject,
                           spread_sheet_id='1X17zc7yRq7o4ge6KreFfQjbxR2B141-Ygx4nCdGeuxI',
                           sheet_list='Результаты',
                           names='A4:A168',
                           grades='D4:D168')

        # DM (34-35 online group)
        self._add_to_table(subject=subject,
                           spread_sheet_id='15pjGIzgfVkVJoXspghvrprrBvPCoJUQbOBA37Et2ChE',
                           sheet_list='Лист1',
                           names='A3:A33',
                           grades='B3:B33')

        # DM (34-35 offline group)
        self._add_to_table(subject=subject,
                           spread_sheet_id='1YOTxFL4CZb0cDhueUFsXEJPa4bM0GMzHBkirJBGsCHw',
                           sheet_list='Лист1',
                           names='A2:A20',
                           grades='B2:B20')
        return self

    def _collect_optimization_methods(self, subject='МетОпт') -> ItmoTable:
        spread_sheet_id = '1F3hoDX6mmFtmBKRiV-iwfp99vetHae5SwB7E-RHrjbY'

        # MetOpt (34 group)
        self._add_to_table(subject=subject,
                           spread_sheet_id=spread_sheet_id,
                           sheet_list='M3234',
                           names='C2:C27',
                           grades='D2:D27')

        # MetOpt (35 group)
        self._add_to_table(subject=subject,
                           spread_sheet_id=spread_sheet_id,
                           sheet_list='M3235',
                           names='C2:C21',
                           grades='D2:D21')

        # MetOpt (36 group)
        self._add_to_table(subject=subject,
                           spread_sheet_id=spread_sheet_id,
                           sheet_list='M3236',
                           names='C2:C26',
                           grades='D2:D26')

        # MetOpt (37 group)
        self._add_to_table(subject=subject,
                           spread_sheet_id=spread_sheet_id,
                           sheet_list='M3237',
                           names='C2:C27',
                           grades='D2:D27')

        # MetOpt (38 group)
        self._add_to_table(subject=subject,
                           spread_sheet_id=spread_sheet_id,
                           sheet_list='M3238',
                           names='C2:C16',
                           grades='D2:D16')

        # MetOpt (39 group)
        self._add_to_table(subject=subject,
                           spread_sheet_id=spread_sheet_id,
                           sheet_list='M3239',
                           names='C2:C20',
                           grades='D2:D20')
        return self

    def _collect_calculus(self, subject='МатАн') -> ItmoTable:
        #  MatAn (34-35, few people from 36-37)
        self._add_to_table(subject=subject,
                           spread_sheet_id='1g4P-QmUCiHH1i-nKb8LBjriSEfGK4mMQdr1h2W2x3n8',
                           sheet_list='All',
                           names='D4:D72',
                           grades='G4:G72')
        return self

    def _collect_java(self, subject='Java') -> ItmoTable:
        # Java (all groups)
        self._add_to_table(subject=subject,
                           spread_sheet_id='1UxWfy2n2osxERr1GvkaYydHBOwMHEUqfjNuwD6RcDQc',
                           sheet_list='java',
                           names='B5:B144',
                           grades='E5:E144')
        return self

    def _add_to_table(self, *, subject: str, spread_sheet_id: str, sheet_list: str,
                      names: str, grades: str, major_dimension: str = "COLUMNS") -> None:
        """
        Adds grades of students to table by getting info using Google Sheets API.

        :param subject: subject from subject_pos dict
        :param spread_sheet_id: id of particular sheet
        :param sheet_list: particular list of sheet
        :param names: range of names of students from sheet
        :param grades: range of grades of students from sheet
        :param major_dimension: what direction data will be taken
        :raises RuntimeError: if something wrong with API
        """

        try:
            # Call the Sheets API
            names = self._sheet.values().get(spreadsheetId=spread_sheet_id,
                                             range=f'{sheet_list}!{names}',
                                             majorDimension=major_dimension).execute().get('values', [])[0]
            grades = self._sheet.values().get(spreadsheetId=spread_sheet_id,
                                              range=f'{sheet_list}!{grades}',
                                              majorDimension=major_dimension).execute().get('values', [])[0]
        except HttpError as err:
            raise err

        for name, grade in zip(names, grades):
            name = ItmoTable._remove_patronymic(name)
            if name not in self._table:
                self._table[name] = [0] * ItmoTable.subjects_count
            self._table[name][ItmoTable.subject_pos[subject]] = ItmoTable._convert_grade(grade)

    @staticmethod
    def _remove_patronymic(name: str) -> str:
        return ' '.join(name.split()[0:2])

    @staticmethod
    def _convert_grade(grade: str) -> float:
        """
        :param grade: grade taken from google sheets (might not always be a valid number)
        :return: float(grade) or 0 if grade cannot be converted to float
        """

        try:
            return float(grade.replace(',', '.'))
        except ValueError:
            return 0


def get_time() -> str:
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_formatted_time_for_file_name() -> str:
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')


def get_last_table() -> str:
    dir_ = 'itmo-tables-samples'
    paths = [os.path.join(os.path.abspath(dir_), file) for file in os.listdir(dir_)]
    latest_file = max(paths, key=os.path.getmtime)
    return latest_file


def get_last_table_name(path: str):
    return path.split('itmo-tables-samples')[1][1:]
