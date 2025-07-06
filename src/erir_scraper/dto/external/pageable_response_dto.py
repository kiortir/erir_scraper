from pydantic import BaseModel


class PageableResponse[T](BaseModel):

    content: list[T]
    totalPages: int
