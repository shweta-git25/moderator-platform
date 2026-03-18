from app.schemas.moderator_schema import BaseResponse


def success_response(message: str, data=None, pagination=None):
    response = BaseResponse(
        success=True,
        message=message,
        data=data,
        pagination=pagination
    )

    return response.model_dump(exclude_none=True)



def error_response(message: str, data=None, pagination=None):
    response = BaseResponse(
        success=False,
        message=message,
        data=data,
        pagination=pagination
    )

    return response.model_dump(exclude_none=True)