from pydantic import BaseModel, HttpUrl


class Field(BaseModel):
    title: str
    value: str
    short: bool


class Context(BaseModel):
    action: str = ""


class Integration(BaseModel):
    url: str
    context: Context


class Actions(BaseModel):
    id: str
    name: str
    type: str | None
    integration: Integration


class Attachment(BaseModel):
    fallback: str | None = None
    color: str | None = None
    pretext: str | None = None
    author_name: str | None = None
    author_link: HttpUrl | None = None
    author_icon: HttpUrl | None = None
    title: str | None = None
    title_link: HttpUrl | None = None
    text: str | None = None
    fields: list[Field] | None = None
    image_url: HttpUrl | None = None
    thumb_url: HttpUrl | None = None
    actions: list[Actions] | None = None
