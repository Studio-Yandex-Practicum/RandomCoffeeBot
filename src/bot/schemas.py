from typing import List, Optional

from pydantic import BaseModel, HttpUrl


class Field(BaseModel):
    title: str
    value: str
    short: bool


class Action(BaseModel):
    id: str
    name: str
    type: str
    integration: dict

    def to_dict(self):
        return dict(self)


class Attachment(BaseModel):
    fallback: Optional[str] = None
    color: Optional[str] = None
    pretext: Optional[str] = None
    author_name: Optional[str] = None
    author_link: Optional[HttpUrl] = None
    author_icon: Optional[HttpUrl] = None
    title: Optional[str] = None
    title_link: Optional[HttpUrl] = None
    text: Optional[str] = None
    fields: Optional[List[Field]] = None
    image_url: Optional[HttpUrl] = None
    thumb_url: Optional[HttpUrl] = None
    actions: Optional[List[dict]] = None

    def to_dict(self):
        return dict(self)
