from typing import List, Optional

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
    fallback: Optional[str]
    color: Optional[str]
    pretext: Optional[str]
    author_name: Optional[str]
    author_link: Optional[HttpUrl]
    author_icon: Optional[HttpUrl]
    title: Optional[str]
    title_link: Optional[HttpUrl]
    text: Optional[str]
    fields: Optional[List[Field]]
    image_url: Optional[HttpUrl]
    thumb_url: Optional[HttpUrl]
    actions: Optional[List[Action]]
