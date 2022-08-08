import math
import urllib.parse
from typing import Dict, Optional, Tuple

from fastapi import Query
from pydantic import BaseModel, validator
from pydantic.dataclasses import dataclass
from starlette.datastructures import URL as StarletteURL


from app.config import PagingConfig

config = PagingConfig()

QueryParamsType = Tuple[Tuple[str, str], ...]


class PaginationParamsConfig:
    allow_population_by_field_name = True


@dataclass(frozen=True, config=PaginationParamsConfig)
class PaginationParams:
    page: int = Query(
        config.DEFAULT_PAGE, ge=config.MIN_PAGE,
        description="Page number", alias=config.PAGE_KEY
    )
    size: int = Query(
        config.DEFAULT_PAGE_SIZE,
        ge=config.MIN_PAGE_SIZE,
        le=config.MAX_PAGE_SIZE,
        description="Page size",
        alias=config.PER_PAGE_KEY,
    )


class PaginationResponseHeaders(BaseModel):
    url: urllib.parse.SplitResult
    page: int
    size: int
    total: int

    class Config:
        frozen = True

    @validator("url", pre=True)
    def _parse_url(cls, v):
        if isinstance(v, StarletteURL):
            v = str(v)
        if isinstance(v, str):
            return urllib.parse.urlsplit(v)
        return v

    def _parse_qsl(self, query_string: str) -> QueryParamsType:
        params = set()
        paging_params = {
            x.alias
            for x
            in PaginationParams.__pydantic_model__.__fields__.values()  # type: ignore  # noqa: E501
        }

        for key, value in urllib.parse.parse_qsl(query_string):
            if key not in paging_params:
                params.add((key, value))

        return tuple(params)

    def _format_links(self) -> str:
        query = self._parse_qsl(self.url.query)

        links = []
        for k, v in self.links.items():
            link_query = [*query, *tuple(v.items())]
            url = self.url._replace(query=urllib.parse.urlencode(link_query))
            formatted = f'<{url.geturl()}>; rel="{k}"'
            links.append(formatted)
        return ", ".join(links)

    @property
    def page_count(self) -> int:
        return max(math.ceil(self.total / self.size), config.MIN_PAGE)

    @property
    def next_num(self) -> Optional[int]:
        return self.page + 1 if self.page < self.page_count else None

    @property
    def prev_num(self) -> Optional[int]:
        return self.page - 1 if self.page >= config.MIN_PAGE else None

    @property
    def links(self) -> Dict[str, Dict[str, int]]:
        links = {
            "self": {
                config.PAGE_KEY: self.page,
                config.PER_PAGE_KEY: self.size,
            },
            "first": {config.PAGE_KEY: 1, config.PER_PAGE_KEY: self.size},
            "last": {
                config.PAGE_KEY: self.page_count,
                config.PER_PAGE_KEY: self.size
            },
        }
        if self.next_num:
            links["next"] = {
                config.PAGE_KEY: self.next_num,
                config.PER_PAGE_KEY: self.size,
            }
        if self.prev_num:
            links["prev"] = {
                config.PAGE_KEY: self.prev_num,
                config.PER_PAGE_KEY: self.size,
            }

        return links

    def headers(self) -> Dict[str, str]:
        return {
            config.TOTAL_COUNT_HEADER: str(self.total),
            config.PAGE_COUNT_HEADER: str(self.page_count),
            config.LINK_HEADER: self._format_links(),
        }
