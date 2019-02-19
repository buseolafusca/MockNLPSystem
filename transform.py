import json
import os
from copy import deepcopy


def transform():
    continuous_dict = {"name": "Count", "datatype": "integer", "measuretype": "continuous", "measuresubtype": "ratio"}
    categorical_dict = {"name": "A&E Diagnosis", "datatype": "string", "measuretype": "categorical",
                        "measuresubtype": "nominal"}

    response_dict = {
        "responseMsg": "SUCCESS",
        "responseCode": "00",
        "responseData": {
            "summary": {
                "question": "",
                "row_count": 4,
                "col_count": 5
            },
            "fields": [],
            "body": []
        }
    }

    folder = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(folder, 'nlp_question_answers_cleaned.json')

    response_list = []

    with open(data_path) as file:
        nlp_raw_json = json.loads(file.read())

    for item in nlp_raw_json:
        buffer_response_dict = deepcopy(response_dict)
        for field in item["result"][0]:
            if field == "Count":
                buffer_continuous_dict = deepcopy(continuous_dict)
                buffer_response_dict["responseData"]["fields"].append(buffer_continuous_dict)
            else:
                buffer_categorical_dict = deepcopy(categorical_dict)
                buffer_categorical_dict["name"] = field
                buffer_response_dict["responseData"]["fields"].append(buffer_categorical_dict)

        buffer_response_dict["responseData"]["body"] = item["result"][1]
        buffer_response_dict["responseData"]["summary"]["question"] = item["question"]
        buffer_response_dict["responseData"]["summary"]["row_count"] = len(item["result"][1])
        buffer_response_dict["responseData"]["summary"]["col_count"] = len(item["result"][0])
        response_list.append(buffer_response_dict)

    return response_list


print(transform())