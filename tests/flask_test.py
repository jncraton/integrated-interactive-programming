"""
Tests for the application's database API

Only tests the program's backend API, not the front-end. 
"""

import pytest
import json
from app import create_app
import time
from datetime import datetime


@pytest.fixture
def client():
    # app.config["TESTING"] = True
    yield create_app(True).test_client()


def test_post_section(client):
    # Test Post Section
    response = client.post(
        "/api/section",
        data=json.dumps(
            {
                "txt_section_name": "Intro to Computer Science",
                "txt_instructor_name": "Professor Smith",
            }
        ),
        mimetype="application/json",
    )

    assert response.json["txt_section_name"] == "Intro to Computer Science"
    assert response.json["txt_instructor_name"] == "Professor Smith"


def test_post_exercise(client):
    # Test Post Exercise
    response = client.post(
        "/api/exercise",
        data=json.dumps(
            {
                "fk_section_id": 0,
                "txt_starting_code": "for i in range(5):",
                "txt_desired_output": "0 1 2 3 4",
            }
        ),
        mimetype="application/json",
    )

    assert response.json["fk_section_id"] == 0
    assert response.json["txt_starting_code"] == "for i in range(5):"
    assert response.json["txt_desired_output"] == "0 1 2 3 4"


def test_post_student(client):
    response = client.post(
        "/api/student",
        data=json.dumps(
            {
                "fk_section_id": 0,
                "txt_student_name": "Bart Simpson",
            }
        ),
        mimetype="application/json",
    )
    assert response.json["fk_section_id"] == 0
    assert response.json["txt_student_name"] == "Bart Simpson"


def test_post_submission(client):
    # Test Post Submission
    response = client.post(
        "/api/submission",
        data=json.dumps(
            {
                "txt_student_program": "for i in range(5): \n\tprint(i)",
                "txt_student_program_output": "1 2 3 4 5",
                "bool_is_complete": True,
                "ts_submission_time": time.mktime(datetime.now().timetuple()),
                "ts_starting_time": time.mktime(datetime.now().timetuple()) - 300,
                "fk_exercise_id": 0,
                "fk_student_id": 0,
            }
        ),
        mimetype="application/json",
    )

    assert response.json["txt_student_program"] == "for i in range(5): \n\tprint(i)"
    assert response.json["txt_student_program_output"] == "1 2 3 4 5"
    assert response.json["bool_is_complete"] == True
    assert response.json["ts_submission_time"] == time.mktime(
        datetime.now().timetuple()
    )
    assert (
        response.json["ts_starting_time"]
        == time.mktime(datetime.now().timetuple()) - 300
    )
    assert response.json["fk_exercise_id"] == 0
    assert response.json["fk_student_id"] == 0

    # Test Get Section


def test_get_section(client):

    response = client.get(
        "/api/section",
        data=json.dumps({"pk_section_id": "1"}),
        mimetype="application/json",
    )

    assert response.json["txt_instructor_name"] == "Dr. Smith"
    assert response.json["txt_section_name"] == "Intro to Programming"

    # Test Get Exercise


def test_get_exercise(client):

    response = client.get(
        "/api/exercise",
        data=json.dumps({"pk_exercise_id": "1"}),
        mimetype="application/json",
    )

    assert response.json["txt_desired_output"] == "Hello World"
    assert response.json["txt_starting_code"] == 'print("Hello World")'

    # Test Get Student


def test_get_student(client):

    response = client.get(
        "/api/student",
        data=json.dumps({"pk_student_id": "1"}),
        mimetype="application/json",
    )

    assert response.json["txt_student_name"] == "Alice"
    # Test Get Submission


def test_get_submission(client):
    response = client.get(
        "/api/submission",
        data=json.dumps({"pk_student_submission_id": "1"}),
        mimetype="application/json",
    )

    assert response.json["ts_starting_time"] == 1694000000
    assert response.json["ts_submission_time"] == 1694000200
    assert response.json["ts_time_recorded"] == 1694000250
    assert response.json["txt_student_program"] == 'print("Hello")'
    assert response.json["txt_student_program_output"] == "Hello"
