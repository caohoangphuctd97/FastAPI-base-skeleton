# from typing import Dict, Union

# from fastapi import status
# import pytest

# from app.config import config
# from app.database.models import Customer, Devices
# from app.schemas import DeviceSchema, CustomerSchema

# from .data.data import CUSTOMER_DATA_PASS

# # All test coroutines will be treated as marked.
# pytestmark = pytest.mark.asyncio

# TEST_DATA_PATH = 'customers.json'
# TEST_HEADERS = {'Authorization': 'Bearer test'}
# # FORBIDDEN_RESPONSE = {'detail': 'Not authenticated'}


# async def test_api_create_customer_passes(client, records):
#     await records(TEST_DATA_PATH)
#     response = await client.post(
#         f'{config.OPENAPI_PREFIX}/customer',
#         json=CUSTOMER_DATA_PASS,
#         headers=TEST_HEADERS)
#     assert response.status_code == status.HTTP_201_CREATED
