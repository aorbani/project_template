import json
import os
import urllib.request
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBasicCredentials , HTTPBearer
security = HTTPBearer()
def get_jwks_url(issuer_url):
    well_known_url = issuer_url + "/.well-known/openid-configuration"
    with urllib.request.urlopen(well_known_url) as response:
        well_known = json.load(response)
    if not 'jwks_uri' in well_known:
        raise Exception('jwks_uri not found in OpenID configuration')
    return well_known['jwks_uri']


async def has_access(credentials: HTTPBasicCredentials = Depends(security)):
    """
        Function that is used to validate the token in the case that it requires it
    """
    token = credentials.credentials
    try:
        unvalidated = jwt.decode(token, options={"verify_signature": False})
        jwks_url = get_jwks_url(unvalidated['iss'])
        jwks_client = jwt.PyJWKClient(jwks_url)
        header = jwt.get_unverified_header(token)
        key = jwks_client.get_signing_key(header["kid"]).key
        payload = jwt.decode(token, key, [header["alg"]], audience = os.getenv('api_aud'))
        in_scope = 'complaints.api.scope' in payload['scope']
        if not in_scope:
            raise Exception("Not authorized. Assistant Apis is not in your scope.")
        print("payload => ", payload)
    except Exception as e:  # catches any exception
        raise HTTPException(
            status_code=401,
            detail=str(e))

async def get_user(credentials: HTTPBasicCredentials = Depends(security)):
    token = credentials.credentials
    try:
        unvalidated = jwt.decode(token, options={"verify_signature": False})
        jwks_url = get_jwks_url(unvalidated['iss'])
        jwks_client = jwt.PyJWKClient(jwks_url)
        header = jwt.get_unverified_header(token)
        key = jwks_client.get_signing_key(header["kid"]).key
        payload = jwt.decode(token, key, [header["alg"]],  audience = os.getenv('api_aud'))
        return payload
    except Exception as e:  # catches any exception
        raise HTTPException(
            status_code=401,
            detail=str(e))
