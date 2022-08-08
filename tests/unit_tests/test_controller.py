import pytest

from typing import Union

from app.controllers.custom_types import (
    ItemHasConstraintError, ItemDoesntExist)
from app.controllers.trigger import (
    create_trigger, search_triggers, get_trigger, update_trigger)
from app.database.models import Trigger
from app.schemas import PostTriggerModel, PatchTriggerModel

from .data.data import (
    TEST_CREATE_TRIGGER_HAPPY_CASE, TEST_CREATE_TRIGGER_NAME_ALREADY_EXISTS,
    TEST_TRIGGER_ID_VALID,
    TEST_PATCH_TRIGGER_MISSING_DATASET_ID)

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio

TEST_DATA_PATH = 'trigger.json'


def check_trigger_result(
     expected: Union[PostTriggerModel, PatchTriggerModel],
     actual: Trigger):
    """Check Trigger result with the expected

    Args:
        expected (Union[PostTriggerModel, PatchTriggerModel]): expected result
        actual (Trigger): actual result
    """
    for key, value in expected.dict(exclude_unset=True).items():
        assert value == getattr(actual, key)


async def test_controller_create_trigger_happy_case_passes(async_session):
    model = PostTriggerModel(**TEST_CREATE_TRIGGER_HAPPY_CASE)
    result = await create_trigger(async_session, model)
    check_trigger_result(model, result)


async def test_controller_create_trigger_name_already_exists_fails(
        async_session, records):
    await records(TEST_DATA_PATH)
    model = PostTriggerModel(**TEST_CREATE_TRIGGER_NAME_ALREADY_EXISTS)
    with pytest.raises(ItemHasConstraintError) as excinfo:
        await create_trigger(async_session, model)
    assert str(excinfo.value) == (
        'Item Trigger has error. '
        f"Trigger with name '{model.name}' already exists in database.")


async def test_controller_search_triggers_no_filter_passes(
        async_session, records):
    test_records = await records(TEST_DATA_PATH)
    results = await search_triggers(async_session)
    assert results.total == len(test_records)


@pytest.mark.parametrize(
    'type,name,signal_type,total,out_ix,in_ix',
    [
        (['STANDARD'], 'GPS Log', ['GPS_LOG_EVENT'], 2, 1, 1),
        (['BUILT_IN', 'CUSTOM'], None, None, 1, None, None),
        (None, 'GPS Log Trigger', None, 2, 1, 1),
        (None, None, ['TRIP_EVENT'], 1, 0, 2)
    ])
async def test_controller_search_triggers_filters_passes(
        async_session, records, type, name, signal_type, total, out_ix, in_ix):
    """Test `search_triggers` controller with filters.

    Args:
        async_session (AsyncSession): asynchronous database session fixture
        records (Callable[str, List[Trigger]]):
            function fixture to populate database with test data
        type (Optional[List[Literal['STANDARD', 'BUILT_IN', 'CUSTOM']]]):
            Trigger type query parameter
        name (Optional[str]): name pattern query parameter
        signal_type (Optional[List[str]], optional):
            list of signal_tpye patterns to filter. Defaults to None.
        total (int): expected total number of search results
        out_ix (Optional[int]): list index of the output record to check
        in_ix (Optional[int]): list index of the input record to check
    """
    test_records = await records(TEST_DATA_PATH)
    results = await search_triggers(async_session, type, name, signal_type)
    assert results.total == total
    if out_ix is not None:
        assert results.records[out_ix] == test_records[in_ix]


@pytest.mark.parametrize(
    'page,page_size,count,out_ix,in_ix',
    [
        (2, 1, 1, 0, 1),
        (1, 2, 2, 1, 1),
        (2, 3, 0, None, None)
    ])
async def test_controller_search_triggers_pagination_passes(
        async_session, records, page, page_size, count, out_ix, in_ix):
    """Test `search_triggers` controller pagination.

    Args:
        async_session (AsyncSession): asynchronous database session fixture
        records (Callable[str, List[Trigger]]):
            function fixture to populate database with test data
        page (int): page query parameter
        page_size (int): page size query parameter
        count (int): expected number of search results in page
        out_ix (Optional[int]): list index of the output record to check
        in_ix (Optional[int]): list index of the input record to check
    """
    test_records = await records(TEST_DATA_PATH)
    results = await search_triggers(
        async_session, page=page, page_size=page_size)
    assert results.total == len(test_records)
    assert results.count == count
    if out_ix is not None:
        assert results.records[out_ix] == test_records[in_ix]


async def test_get_trigger_happy_case(async_session, records):
    """Test controller get Trigger happy case

    Args:
        async_session (AsyncSession): asynchronous database session fixture
        records (Callable[str, List[Trigger]]):
            function fixture to populate database with test data
    """

    # fetched record happy case
    test_records = await records(TEST_DATA_PATH)
    for record in test_records[:2]:
        record_fetched = await get_trigger(async_session, record.id_)
        assert record_fetched == record


async def test_get_trigger_not_found(async_session, records):
    """Test controller get Trigger not found

    Args:
        async_session (AsyncSession): asynchronous database session fixture
        records (Callable[str, List[Trigger]]):
            function fixture to populate database with test data
    """

    await records(TEST_DATA_PATH)

    # fetched record not found in database
    with pytest.raises(ItemDoesntExist) as excinfo:
        await get_trigger(async_session, TEST_TRIGGER_ID_VALID)
    assert str(excinfo.value) == \
        f"Item Trigger with id {TEST_TRIGGER_ID_VALID} not found."


async def test_controll_update_trigger_happy_case(
        client, async_session, records):
    test_records = await records(TEST_DATA_PATH)
    model = PatchTriggerModel(**TEST_CREATE_TRIGGER_HAPPY_CASE)
    await update_trigger(
        async_session, test_records[0].id_, model)
    actual_obj = await get_trigger(async_session, test_records[0].id_)
    check_trigger_result(model, actual_obj)


@pytest.mark.parametrize(
    'test_data,errors',
    [
        (
            TEST_CREATE_TRIGGER_NAME_ALREADY_EXISTS,
            "Trigger with name"
        ),
        (
            TEST_PATCH_TRIGGER_MISSING_DATASET_ID,
            "dataset_id only nullable for BUILT_IN triggers"
        )
    ])
async def test_controll_update_trigger_validation_error_fails(
        records, async_session, test_data, errors):
    test_records = await records(TEST_DATA_PATH)
    model = PatchTriggerModel(**test_data)
    with pytest.raises(ItemHasConstraintError) as excinfo:
        await update_trigger(
            async_session, test_records[2].id_, model)
    assert errors in str(excinfo.value)
