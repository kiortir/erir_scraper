import datetime
import csv
from io import StringIO
import json
from typing import Any
from fastapi import Body, Depends, FastAPI, Request
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from dependencies import get_service
from dto.external.invoice_response_dto import InvoiceResponseDto


from service.erir_scraper import ErirScraperService

origins = [
    "https://erir.grfc.ru",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def to_datetime(
    date_obj: datetime.date, to_end: bool = False
) -> datetime.datetime:
    year = date_obj.year
    month = date_obj.month
    day = date_obj.day
    if to_end:
        hour = 23
        minute = 59
        second = 59
        microsecond = 999
    else:
        hour = 0
        minute = 0
        second = 0
        microsecond = 0
    return datetime.datetime(
        year, month, day, hour, minute, second, microsecond
    )


async def generator(page_1, filters, repository):
    with StringIO() as io:
        writer = csv.DictWriter(
            io, fieldnames=InvoiceResponseDto.model_fields, delimiter=";"
        )
        writer.writeheader()
        c = [row.model_dump(mode="json") for row in page_1.content]
        writer.writerows(c)
        total_pages = page_1.totalPages
        print(total_pages)
        for page_idx in range(1, total_pages):
            page = await repository.get_invoice_list(
                filters, page=page_idx, page_size=200000
            )
            c = [row.model_dump(mode="json") for row in page.content]
            writer.writerows(c)

        yield io.getvalue().encode("utf-8-sig")


@app.post("/export/invoices")
def export_invoices(
    body: Any = Body(),
    service: ErirScraperService = Depends(get_service),
):
    filters = json.loads(body)

    fields = [
        "invoiceNumber",
        "invoiceDate",
        "periodFrom",
        "periodTo",
        "ordCreateDate",
    ]

    return StreamingResponse(
        service.get_content_as_xlsx_with_filters(
            filters=filters, fields=fields
        ),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
