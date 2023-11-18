

def single_user_schema():
    expected_schema = {
          "type": "object",
          "properties": {
            "id": {
              "type": "integer"
            },
            "name": {
              "type": "string"
            },
            "email": {
              "type": "string"
            },
            "gender": {
              "type": "string"
            },
            "status": {
              "type": "string"
            }
          },
          "required": [
            "id",
            "name",
            "email",
            "gender",
            "status"
          ]
        }
    return expected_schema


def single_post_schema():
    expected_schema = {
          "type": "object",
          "properties": {
            "id": {
              "type": "integer"
            },
            "user_id": {
              "type": "integer"
            },
            "title": {
              "type": "string"
            },
            "body": {
              "type": "string"
            }
          },
          "required": [
            "id",
            "user_id",
            "title",
            "body"
          ]
        }
    return expected_schema
