from typing import List

from pydantic import BaseModel, HttpUrl


class Field(BaseModel):
    title: str
    value: str
    short: bool


class Action(BaseModel):
    name: str
    text: str
    type: str
    value: str


class Attachment(BaseModel):
    fallback: str | None
    color: str | None
    pretext: str | None
    author_name: str | None
    author_link: HttpUrl | None
    author_icon: HttpUrl | None
    title: str | None
    title_link: HttpUrl | None
    text: str | None
    fields: List[Field] | None
    image_url: HttpUrl | None
    thumb_url: HttpUrl | None
    actions: List[Action] | None
