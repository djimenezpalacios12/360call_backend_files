from app.schemas.token import TokenModel
from app.core.verify_access_token.token_validation import verify_access_token


def decode_token(request):
    decoded_token = verify_access_token(request)
    data_token = TokenModel(**decoded_token)

    return data_token
