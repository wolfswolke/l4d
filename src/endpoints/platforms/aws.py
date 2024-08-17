from flask_definitions import *
# REQ:
# {
#   "body": [
#     {
#       "timestamp": 1686251652,
#       "eventType": "gm_session_started",
#       "eventTypeVersion": 1,
#       "userId": "<user_id>",
#       "eventId": "<event_id>",
#       "data": {
#         "event_id": "<event_id>",
#         "event_type": "gm_session_started",
#         "event_time": "2023-06-08T19:14:12.184Z",
#         "event_order": 1,
#         "session_id": "<session_id>"
#       }
#     },
#     {
#       "timestamp": 1686251667,
#       "eventType": "gm_session_ended",
#       "eventTypeVersion": 1,
#       "userId": "<user_id>",
#       "eventId": "<event_id>",
#       "data": {
#         "event_id": "<event_id>",
#         "event_type": "gm_session_ended",
#         "event_time": "2023-06-08T19:14:27.978Z",
#         "event_order": 2,
#         "session_id": "<session_id>"
#       }
#     }
#   ]
# }

# Response:
# {
#     "RecordId": "495b3e4f-7b0d-4f3b-8b0b-1b1b4b4b4b4b",
# }
# Response on array:
# {
#     "FailedPutCount": 0,
#     "RequestResponse": [
#         {
#             "RecordId": "495b3e4f-7b0d-4f3b-8b0b-1b1b4b4b4b4b",
#         }
#     ]
# }

temp_records = []


@app.route('/api/v1/aws/<index>/batch', methods=['POST'])
def aws_batch(index):
    try:
        records = []
        resp = {
            "FailedPutCount": 0,
            "RequestResponses": []
        }
        data = request.json['body']
        for item in data:
            record_id = firehose_generator.generate()
            resp['RequestResponses'].append({"RecordId": record_id})
            logger.log(level="info", handler="aws", content=f"index: {index} data: {item}, record_id: {record_id}")
            records.append({"index": index, "data": item, "record_id": record_id})
        mongo.add_batch("firehose", data)
        return jsonify(records)
    except Exception as e:
        logger.log_exception(e)
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500


@app.route('/temp/firehose', methods=['GET'])
def firehose():
    return jsonify(temp_records)
