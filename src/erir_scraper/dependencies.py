from typing import Annotated
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import httpx

from clients.auth.erir_token import TokenAuth
from repository.erir import ErirRepository
from service.erir_scraper import ErirScraperService


security = HTTPBearer()


async def get_auth(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    auth = TokenAuth(credentials.credentials)
    return auth


async def get_repository(auth: httpx.Auth = Depends(get_auth)):
    client = httpx.Client(auth=auth, base_url="https://erir.grfc.ru")
    repository = ErirRepository(client)
    return repository


async def get_service(repository: ErirRepository = Depends(get_repository)):
    service = ErirScraperService(repository)
    return service
