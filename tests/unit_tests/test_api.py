from typing import Dict, Union

from fastapi import status
import pytest

from app.config import config
from app.database.models import Trigger
from app.schemas import PostTriggerModel, TriggerModel, PatchTriggerModel

from .data.data import (
    TEST_CREATE_TRIGGER_HAPPY_CASE, TEST_CREATE_TRIGGER_INVALID_TYPES,
    TEST_CREATE_TRIGGER_MISSING_DATASET_ID,
    TEST_CREATE_TRIGGER_NAME_ALREADY_EXISTS,
    TEST_CREATE_TRIGGER_SIGNAL_OBJECT_NOT_MACHING_TYPE,
    TEST_TRIGGER_ID_INVALID, TEST_TRIGGER_ID_VALID,
    TEST_TRIGGER_TYPE_INVALID, TEST_TRIGGER_TYPE_VALID,
    TEST_TRIGGER_SIGNAL_TYPE_VALID, TEST_TRIGGER_SIGNAL_TYPE_INVALID,
    TEST_PATCH_TRIGGER_INVALID_TYPES,
    TEST_PATCH_TRIGGER_MISSING_DATASET_ID,
    TEST_PATCH_TRIGGER_SIGNAL_OBJECT_NOT_MACHING_TYPE)

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio

TEST_DATA_PATH = 'trigger.json'
TEST_HEADERS = {'Authorization': 'Bearer test'}
FORBIDDEN_RESPONSE = {'detail': 'Not authenticated'}


def check_trigger_record(
     output_obj: Dict, input_obj: Union[Dict, Trigger, TriggerModel]):
    """Check if certain fields of Trigger output match those of Trigger input

    Args:
        output_obj (Dict): output dictionary
        input_obj (Union[Dict, Trigger, TriggerModel]): input object
    """
    output_converted: Union[PostTriggerModel, TriggerModel] = \
        TriggerModel.parse_obj(output_obj) \
        if 'id' in output_obj \
        else PostTriggerModel.parse_obj(output_obj)
    input_converted: Union[PostTriggerModel, Trigger]
    if isinstance(input_obj, Dict):
        input_converted = PostTriggerModel.parse_obj(input_obj)
    elif isinstance(input_obj, TriggerModel):
        input_converted = input_obj
    elif isinstance(output_converted, TriggerModel):
        input_converted = input_obj
        assert output_converted.id_ == input_converted.id_
    for field in ['name', 'type', 'signal_type', 'signal_config']:
        if getattr(input_converted, field) is not None:
            assert getattr(output_converted, field) == \
                getattr(input_converted, field)


async def test_api_create_trigger_passes(client):
    response = await client.post(
        f'{config.OPENAPI_PREFIX}/triggers',
        json=TEST_CREATE_TRIGGER_HAPPY_CASE,
        headers=TEST_HEADERS)
    assert response.status_code == status.HTTP_201_CREATED
    check_trigger_record(response.json(), TEST_CREATE_TRIGGER_HAPPY_CASE)


async def test_api_create_trigger_name_already_exists_fails(client, records):
    await records(TEST_DATA_PATH)
    response = await client.post(
        f'{config.OPENAPI_PREFIX}/triggers',
        json=TEST_CREATE_TRIGGER_NAME_ALREADY_EXISTS,
        headers=TEST_HEADERS)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['content'] == (
        'Item Trigger has error. Trigger with name '
        f"'{TEST_CREATE_TRIGGER_NAME_ALREADY_EXISTS['name']}' "
        'already exists in database.')


@pytest.mark.parametrize(
    'test_data,num_errors',
    [
        (TEST_CREATE_TRIGGER_INVALID_TYPES, 2),
        (TEST_CREATE_TRIGGER_MISSING_DATASET_ID, 1),
        # PGN_SEGMENT has 6 top-level and 1 sub-level (of `samplingConfig`)
        # fields that a GPS_LOG_EVENT signal object doesn't have, so 7 errors
        (TEST_CREATE_TRIGGER_SIGNAL_OBJECT_NOT_MACHING_TYPE, 7)
    ])
async def test_api_create_trigger_validation_error_fails(
        client, test_data, num_errors):
    response = await client.post(
        f'{config.OPENAPI_PREFIX}/triggers',
        json=test_data,
        headers=TEST_HEADERS)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json()['detail']) == num_errors


async def test_api_create_trigger_unauthorized_fails(client):
    response = await client.post(
        f'{config.OPENAPI_PREFIX}/triggers',
        json=TEST_CREATE_TRIGGER_HAPPY_CASE)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == FORBIDDEN_RESPONSE


async def test_api_search_triggers_no_filter_passes(client, records):
    test_records = await records(TEST_DATA_PATH)
    response = await client.get(
        f'{config.OPENAPI_PREFIX}/triggers', headers=TEST_HEADERS)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(test_records)


async def test_api_search_triggers_found_passes(client, records):
    test_records = await records(TEST_DATA_PATH)
    response = await client.get(
        f'{config.OPENAPI_PREFIX}/triggers?'
        f"type={test_records[0].type}&name=Standard GPS Log&"
        f"signalType={test_records[0].signal_type}",
        headers=TEST_HEADERS)
    assert response.status_code == status.HTTP_200_OK
    records_json = response.json()
    assert len(records_json) == 1
    check_trigger_record(records_json[0], test_records[0])


async def test_api_search_triggers_not_found_passes(client):
    response = await client.get(
        f'{config.OPENAPI_PREFIX}/triggers?type={TEST_TRIGGER_TYPE_VALID}&'
        f'signalType={TEST_TRIGGER_SIGNAL_TYPE_VALID}',
        headers=TEST_HEADERS)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 0


@pytest.mark.parametrize(
    'page,per_page,count,page_count,out_ix,in_ix',
    [
        (2, 1, 1, '3', 0, 1),
        (1, 2, 2, '2', 1, 1),
        (2, 3, 0, '1', None, None)
    ])
async def test_api_search_triggers_pagination_passes(
        client, records, page, per_page, count, page_count, out_ix, in_ix):
    """Test `search_triggers` endpoint pagination.

    Args:
        client (async_asgi_testclient.TestClient): asynchronous test client
        records (Callable[str, List[Trigger]]):
            function fixture to populate database with test data
        page (int): page query parameter
        per_page (int): page size query parameter
        count (int): expected number of search results in page
        page_count (str): string representing expected number of pages
        out_ix (Optional[int]): list index of the output record to check
        in_ix (Optional[int]): list index of the input record to check
    """
    test_records = await records(TEST_DATA_PATH)
    response = await client.get(
        f'{config.OPENAPI_PREFIX}/triggers?page={page}&per_page={per_page}',
        headers=TEST_HEADERS)
    assert response.status_code == status.HTTP_200_OK
    records_json = response.json()
    assert len(records_json) == count
    if out_ix is not None:
        check_trigger_record(records_json[out_ix], test_records[in_ix])
    assert response.headers[config.paging.PAGE_COUNT_HEADER] == page_count
    assert response.headers[config.paging.TOTAL_COUNT_HEADER] \
        == str(len(test_records))
    assert config.paging.LINK_HEADER in response.headers


async def test_api_search_triggers_invalid_type_params_fails(client):
    response = await client.get(
        f'{config.OPENAPI_PREFIX}/triggers?'
        f'type={TEST_TRIGGER_TYPE_INVALID}&name=string',
        headers=TEST_HEADERS)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json()['detail']) == 1


async def test_api_search_triggers_invalid_signal_type_params_fails(client):
    response = await client.get(
        f'{config.OPENAPI_PREFIX}/triggers?'
        f'signalType={TEST_TRIGGER_SIGNAL_TYPE_INVALID}&name=string',
        headers=TEST_HEADERS)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json()['detail']) == 1


async def test_api_search_triggers_unauthorized_fails(client):
    response = await client.get(
        f'{config.OPENAPI_PREFIX}/triggers?type={TEST_TRIGGER_TYPE_VALID}')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == FORBIDDEN_RESPONSE


async def test_api_get_trigger_passes(client, records):
    test_records = await records(TEST_DATA_PATH)
    response = await client.get(
        f'{config.OPENAPI_PREFIX}/triggers/{test_records[0].id_}',
        headers=TEST_HEADERS)
    assert response.status_code == status.HTTP_200_OK
    check_trigger_record(response.json(), test_records[0])


async def test_api_get_trigger_not_found_fails(client):
    response = await client.get(
        f'{config.OPENAPI_PREFIX}/triggers/{TEST_TRIGGER_ID_VALID}',
        headers=TEST_HEADERS)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()['detail'] == \
        f'Item Trigger with id {TEST_TRIGGER_ID_VALID} not found.'


async def test_api_get_trigger_invalid_param_fails(client):
    response = await client.get(
        f'{config.OPENAPI_PREFIX}/triggers/{TEST_TRIGGER_ID_INVALID}',
        headers=TEST_HEADERS)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json()['detail']) == 1


async def test_api_get_trigger_unauthorized_fails(client, records):
    test_records = await records(TEST_DATA_PATH)
    response = await client.get(
        f'{config.OPENAPI_PREFIX}/triggers/{test_records[0].id_}')
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == FORBIDDEN_RESPONSE


async def test_api_update_trigger_passes(client, records):
    test_records = await records(TEST_DATA_PATH)
    response = await client.patch(
        f'{config.OPENAPI_PREFIX}/triggers/{test_records[0].id_}',
        json=TEST_CREATE_TRIGGER_HAPPY_CASE,
        headers=TEST_HEADERS)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    model = PatchTriggerModel(**TEST_CREATE_TRIGGER_HAPPY_CASE)
    response = await client.get(
        f'{config.OPENAPI_PREFIX}/triggers/{test_records[0].id_}',
        headers=TEST_HEADERS)
    input_obj = TriggerModel(**response.json())
    check_trigger_record(model.dict(), input_obj)


async def test_api_update_trigger_unauthorized_fails(client, records):
    test_records = await records(TEST_DATA_PATH)
    response = await client.patch(
            f'{config.OPENAPI_PREFIX}/triggers/{test_records[0].id_}',
            json=TEST_CREATE_TRIGGER_HAPPY_CASE)
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == FORBIDDEN_RESPONSE


@pytest.mark.parametrize(
    'test_data,num_errors',
    [
        (TEST_PATCH_TRIGGER_INVALID_TYPES, 3),
        (TEST_PATCH_TRIGGER_SIGNAL_OBJECT_NOT_MACHING_TYPE, 7)
    ])
async def test_api_update_trigger_validation_error_fails(
        client, records, test_data, num_errors):
    test_records = await records(TEST_DATA_PATH)
    response = await client.patch(
        f'{config.OPENAPI_PREFIX}/triggers/{test_records[2].id_}',
        json=test_data,
        headers=TEST_HEADERS)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json()['detail']) == num_errors


async def test_api_update_trigger_missing_dataset_id(client, records):
    test_records = await records(TEST_DATA_PATH)
    response = await client.patch(
        f'{config.OPENAPI_PREFIX}/triggers/{test_records[2].id_}',
        json=TEST_PATCH_TRIGGER_MISSING_DATASET_ID,
        headers=TEST_HEADERS)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['content'] == \
        'Item Trigger has error. dataset_id only nullable for BUILT_IN triggers'    # noqa: E501


async def test_api_update_trigger_when_name_already_exists_fails(
        client, records):
    test_records = await records(TEST_DATA_PATH)
    TEST_CREATE_TRIGGER_NAME_ALREADY_EXISTS["name"] = test_records[1].name
    response = await client.patch(
            f'{config.OPENAPI_PREFIX}/triggers/{test_records[0].id_}',
            json=TEST_CREATE_TRIGGER_NAME_ALREADY_EXISTS,
            headers=TEST_HEADERS)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['content'] == (
        'Item Trigger has error. Trigger with name '
        f"'{TEST_CREATE_TRIGGER_NAME_ALREADY_EXISTS['name']}' "
        'already exists in database.')
