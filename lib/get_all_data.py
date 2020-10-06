from __future__ import annotations
from .connection import Connection
from .query_template import query_survey_table
from .query_template import query_question_table
from .query_template import set_null_column
from .query_template import answer_query
from .query_template import outer_union_query
import pandas as pd


def get_all_data_survey(db_connection: Connection) -> str:
    """
    Objective
    ---------

    Function designed to return the string of our SQL procedure. The whole
    procedure to get the string mainly relies on the extraction of the data
    as pandas DataFrames from which we iterate to get the expected columns
    and values. Building this string will help us to obtain a table of the
    format:

    +----------+----------+----------+----------+----------+
    |   UserId | SurveyId |  ANS_Q1  |  ANS_Q2  |  ANS_Q3  |
    +----------+----------+----------+----------+----------+

    Parameters
    ----------
    - db_connection: Connection object to talk to the MSSQL Database server

    Return
    ------
    - final_sql_query: string
    """
    survey_table = pd.read_sql(query_survey_table(), db_connection)
    final_sql_query = ""
    survey_id = None

    counter_1 = 0
    for id_survey, _, _ in survey_table.itertuples(index=False):
        survey_id = id_survey
        column_query_part = ""
        question_table = pd.read_sql(
            query_question_table(survey_id), db_connection
            )

        counter_2 = 0
        for _, question_id, question_in_survey in question_table.itertuples(index=False):
            if question_in_survey == 0:
                column_query_part += set_null_column(question_id)
            else:
                column_query_part += answer_query(survey_id, question_id)

            if counter_2 != len(question_table) - 1:
                column_query_part += " , "
                counter_2 += 1

        current_union_query = outer_union_query(survey_id, column_query_part)
        final_sql_query += current_union_query

        if counter_1 != len(survey_table) - 1:
            final_sql_query += " UNION "
            counter_1 += 1

    return final_sql_query
