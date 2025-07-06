import datetime
from pydantic import BaseModel, Field, field_serializer


class InvoiceResponseDto(BaseModel):
    invoiceNumber: str = Field(title="Номер акта")
    invoiceDate: datetime.date = Field(title="Дата акта")
    periodFrom: datetime.date = Field(title="Период с", )
    periodTo: datetime.date = Field(title="Период по")
    amount: float = Field(title="Сумма (₽)")
    isVat: bool = Field(title="С НДС")
    ordId: str = Field(title="ID акта в ОРД")
    ordName: str = Field(title="")
    externalId: str = Field(title="")
    contractId: str = Field(title="")
    contractInfo: str = Field(title="Название договора")
    description: str = Field(title="")
    createdBy: str = Field(title="")
    createdDate: datetime.datetime = Field(
        title="Дата регистрации изменений в ЕРИР"
    )
    clientName: str = Field(title="Заказчик")
    clientInn: str = Field(title="ИНН заказчика")
    contractorName: str = Field(title="Исполнитель")
    contractorInn: str = Field(title="ИНН Исполнителя")
    clientRoleCode: str = Field(title="Код роли заказчика")
    contractorRoleCode: str = Field(title="Код роли исполнителя")
    reporterName: str = Field(title="Поставщик данных")
    reporterInn: str = Field(title="ИНН поставщика данных")
    ordCreateDate: datetime.datetime = Field(title="Дата регистрации в ОРД")
    ordUpdateDate: datetime.datetime = Field(title="Дата изменений в ОРД")
    isDeallocation: bool = Field(title="")
    deallocationQnt: int = Field(title="")
    deallocationSum: float = Field(title="")
