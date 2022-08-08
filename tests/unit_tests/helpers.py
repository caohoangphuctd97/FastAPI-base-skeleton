import json
from pathlib import Path
from typing import Dict, Union, List

from sqlalchemy.ext.asyncio import AsyncSession

from app import controllers
from app.database.models import Trigger
from app.schemas import PostTriggerModel

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


def table_records(path: str) -> List[PostTriggerModel]:
    records = []
    for record in load_data(path):
        records.append(PostTriggerModel.parse_obj(record))
    return records


async def populate_db(session: AsyncSession, path: str) -> List[Trigger]:
    records = table_records(path)
    db_records = []

    for record in records:
        db_record = await controllers.trigger.create_trigger(session, record)
        db_records.append(db_record)

    return db_records
