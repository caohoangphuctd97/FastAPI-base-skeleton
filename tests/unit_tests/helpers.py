import json
from pathlib import Path
from typing import Dict, Union, List

from sqlalchemy.ext.asyncio import AsyncSession

from app import controllers
from app.database.models import Customer
from app.schemas import DeviceSchema, CustomerSchema

DATA_ROOT = Path(__file__).parent / "data"
JsonType = Dict[str, object]


def load_data(path: str, as_json: bool = True) -> Union[str, JsonType]:
    if not path.endswith(".json"):
        path += ".json"

    with open(DATA_ROOT / path) as f:
        if as_json:
            return json.load(f)
        else:
            return f.read()


def table_records(path: str) -> List[CustomerSchema]:
    records = []
    for record in load_data(path):
        records.append(CustomerSchema.parse_obj(record))
    return records


async def populate_db(session: AsyncSession, path: str) -> List[Customer]:
    records = table_records(path)
    db_records = []

    for record in records:
        db_record = await controllers.customers.create_customer(session, record)
        db_records.append(db_record)

    return db_records
