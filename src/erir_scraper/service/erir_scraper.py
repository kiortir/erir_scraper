from functools import wraps
import time

from io import BytesIO
from typing import Any
import pandas as pd
from dto.external.invoice_response_dto import InvoiceResponseDto
from repository.erir import ErirRepository


class ErirScraperService:

    def __init__(self, repository: ErirRepository) -> None:
        self.repository = repository

    def get_content_with_filters(self, filters: dict[str, Any]):
        total_pages = 1
        page = 0
        while page < total_pages:
            page_data = self.repository.get_invoice_list(
                filters, page, page_size=250_000
            )

            yield page_data.content
            total_pages = page_data.totalPages
            page += 1

    def get_content_as_xlsx_with_filters(
        self, fields: list[str], filters: dict[str, Any]
    ):
        header = [
            field_meta.title or field_name
            for field_name, field_meta in InvoiceResponseDto.model_fields.items()
            if field_name in fields
        ]
        df = pd.DataFrame(columns=fields)
        for page in self.get_content_with_filters(filters):
            page_df = pd.DataFrame(
                (vars(invoice) for invoice in page), columns=fields
            )
            if not len(df):
                df = page_df
            else:
                df = pd.concat((df, page_df), ignore_index=True)

        with BytesIO() as buffer:
            df.to_excel(buffer, header=header)
            yield buffer.getvalue()
