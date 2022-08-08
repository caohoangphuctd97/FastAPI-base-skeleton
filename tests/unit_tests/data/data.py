TEST_CREATE_TRIGGER_HAPPY_CASE = {
    'name': 'Test Trigger',
    'description': 'A test trigger',
    'type': 'STANDARD',
    'datasetId': '9a551bf4-d816-4425-8e00-12a0203183d6',
    'signalType': 'PGN_SEGMENT',
    'signalConfig': {
        'pgn': 12345,
        'source': 0,
        'channel': 'CHAN0',
        'offset': 0,
        'length': 8,
        'samplingConfig': {
            'rearmTime': 3,
            'sampleTime': 3
        },
        'operationConfig': {
            'operator': 'OP_EQUAL_TO',
            'comparedValue': 0
        }
    }
}
TEST_PGN_SEGMENT_SIGNAL_BODY = {
    'signalConfig': {
        'pgn': 12345,
        'source': 0,
        'channel': 'CHAN0',
        'offset': 0,
        'length': 8,
        'samplingConfig': {
            'rearmTime': 3,
            'sampleTime': 3
        },
        'operationConfig': {
            'operator': 'OP_EQUAL_TO',
            'comparedValue': 0
        }
    }
}
TEST_GPS_LOG_EVENT_SIGNAL_BODY = {
    'signalType': 'GPS_LOG_EVENT',
    'signalConfig': {
        'eventType': 'EVENT_POINT_LOGGED',
        'samplingConfig': {
            'rearmTime': 5
        }
    }
}
TEST_CREATE_TRIGGER_NAME_ALREADY_EXISTS = {
    'name': 'Another one',
    'description': 'Another one but it already exists',
    'type': 'BUILT_IN',
    **TEST_GPS_LOG_EVENT_SIGNAL_BODY    # type: ignore
}
TEST_CREATE_TRIGGER_INVALID_TYPES = {
    'name': 'Invalid types',
    'description': 'Invalid trigger type and signal type',
    'type': 'INVALID_TYPE',
    'datasetId': '9a551bf4-d816-4425-8e00-12a0203183d6',
    **TEST_GPS_LOG_EVENT_SIGNAL_BODY,   # type: ignore
    'signalType': 'INVALID_SIGNAL_TYPE'
}
TEST_CREATE_TRIGGER_MISSING_DATASET_ID = {
    'name': 'Missing Dataset ID',
    'description': 'Missing Dataset ID',
    'type': 'STANDARD',
    **TEST_GPS_LOG_EVENT_SIGNAL_BODY    # type: ignore
}
TEST_CREATE_TRIGGER_SIGNAL_OBJECT_NOT_MACHING_TYPE = {
    'name': 'Object not matching type',
    'description': 'Signal object is of different type than declared',
    'type': 'STANDARD',
    'datasetId': '9a551bf4-d816-4425-8e00-12a0203183d6',
    **TEST_GPS_LOG_EVENT_SIGNAL_BODY,   # type: ignore
    'signalType': 'PGN_SEGMENT'
}
TEST_TRIGGER_ID_VALID = 'df911a78-a1eb-469f-a0cb-a082589408a0'
TEST_TRIGGER_ID_INVALID = '0'
TEST_TRIGGER_TYPE_VALID = "STANDARD"
TEST_TRIGGER_TYPE_INVALID = "INVALID"
TEST_TRIGGER_SIGNAL_TYPE_VALID = "PGN_SEGMENT"
TEST_TRIGGER_SIGNAL_TYPE_INVALID = "INVALID"

TEST_PATCH_TRIGGER_INVALID_TYPES = {
    'name': 'Invalid types',
    'description': 'Invalid trigger type and signal type',
    'type': 'INVALID_TYPE',
    'datasetId': '9a551bf4-d816-4425-8e00-12a0203183d6',
    'signalType': 'INVALID_SIGNAL_TYPE',
    **TEST_PGN_SEGMENT_SIGNAL_BODY,   # type: ignore
}
TEST_PATCH_TRIGGER_MISSING_DATASET_ID = {
    'name': 'Missing Dataset ID',
    'description': 'Missing Dataset ID',
    'type': 'STANDARD',
    'datasetId': None,
    'signalType': 'PGN_SEGMENT',
    **TEST_PGN_SEGMENT_SIGNAL_BODY    # type: ignore
}
TEST_PATCH_TRIGGER_SIGNAL_OBJECT_NOT_MACHING_TYPE = {
    'name': 'Object not matching type',
    'description': 'Signal object is of different type than declared',
    'type': 'STANDARD',
    'datasetId': '9a551bf4-d816-4425-8e00-12a0203183d6',
    **TEST_GPS_LOG_EVENT_SIGNAL_BODY,   # type: ignore
    'signalType': 'BUILTIN_SPN_SEGMENT'
}
