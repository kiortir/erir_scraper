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
