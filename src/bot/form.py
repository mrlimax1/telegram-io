from src.api.models.Answers import DataAnswers
from pydantic import Json


def text_form(data: Json):
    data = DataAnswers.parse_raw(data)
    t = "" + data.other + "\n\n" if data.other is not None else ''
    t += "Телефон: " + str(data.tel) + "\n\n" if data.tel is not None else ''
    t += "Почта: " + str(data.email) if data.email is not None else ''
    return t
