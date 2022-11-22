from fastapi import HTTPException
from fastapi import status

import dependencies.user as user

def exception_409(exception_text: str):
    exception = HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"{exception_text}"
                    )
    raise exception


def exception_409_user(username: str | None = None, email: str | None = None):
    if user.get_user(username=username):
        exception_text = 'User with the same username already exists'
        exception = HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"{exception_text}"
                        )
        raise exception

    if user.get_user(email=email):
        exception_text = 'User with the same email already exists'
        exception = HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=f"{exception_text}"
                        )
        raise exception