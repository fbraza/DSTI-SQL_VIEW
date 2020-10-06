def outer_union_query(survey_id, question_answers):
    return """ SELECT UserId
                     , {0} AS SurveyId
                     , {1}
                FROM [User] AS u
                WHERE EXISTS
                    (
                        SELECT *
                            FROM Answer as a
                            WHERE u.UserId = a.UserId
                            AND a.SurveyId = {0}
                     ) """.format(survey_id, question_answers)


def answer_query(survey_id, question_id):
    return """ COALESCE((SELECT a.Answer_Value
                            FROM Answer as a
                            WHERE a.UserId = u.UserId
                            AND a.SurveyId = {0}
                            AND a.QuestionId = {1}),
                            -1) AS ANS_Q{1} """.format(survey_id, question_id)


def set_null_column(question_id):
    return " NULL AS ANS_Q{0} ".format(question_id)


def query_survey_table():
    return " SELECT * FROM Survey_Sample_A18.dbo.Survey "


def query_question_table(survey_id):
    return """ SELECT *
                FROM (SELECT SurveyId, QuestionId, 1 AS InSurvey
                      FROM SurveyStructure WHERE SurveyId = {0}
                      UNION
                      SELECT {0} AS SurveyId, Q.QuestionId, 0 as InSurvey
                      FROM Question as Q WHERE NOT EXISTS
                        (SELECT *
                         FROM SurveyStructure as S
                         WHERE S.SurveyId = {0}
                         AND S.QuestionId = Q.QuestionId)) AS T
                         ORDER BY QuestionId """.format(survey_id)
