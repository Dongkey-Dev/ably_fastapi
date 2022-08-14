from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPBearer


class OptionalHTTPBearer(HTTPBearer):
    async def __call__(self, request: Request):
        from fastapi import status
        try:
            r = await super().__call__(request)
            token = r.credentials
        except HTTPException as ex:
            assert ex.status_code == status.HTTP_403_FORBIDDEN, ex
            token = None
        return token


auth_scheme = OptionalHTTPBearer()
