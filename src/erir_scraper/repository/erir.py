from typing import Any

import httpx
from dto.external.filtered_request_dto import FilterRequestBody
from dto.external.pageable_response_dto import PageableResponse
from dto.external.invoice_response_dto import InvoiceResponseDto


class ErirRepository:

    def __init__(self, client: httpx.Client) -> None:
        self.client = client

    def get_invoice_list(
        self, filters: dict[str, Any], page: int = 0, page_size: int = 1000
    ):
        url = "/register-service/v2/private/api/v-invoice-report/filter"
        request_body = FilterRequestBody(
            page=page, size=page_size
        ).model_dump(mode="json")
        request_body |= filters
        data_response = self.client.post(url, json=request_body)
        data_response.raise_for_status()
        response = PageableResponse[InvoiceResponseDto].model_validate_json(
            data_response.content
        )
        return response
