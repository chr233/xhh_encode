from encode import hkeyencode as enc1
from encode2 import hkeyencode as enc2
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import RedirectResponse, Response
from fastapi.params import Query
from fastapi import FastAPI
from re import compile

app = FastAPI()

Matcher = compile(r'^[a-zA-Z0-9]{32}$')


class BaseResponse(BaseModel):
    msg: Optional[str]
    success: bool = False


@app.get("/")
@app.post("/")
async def index():
    return RedirectResponse("https://blog.chrxw.com/", 302)


@app.get("/encode")
@app.post("/encode")
async def encode(urlpath: str = Query(None), timestamp: str = Query(None), nonce: str = Query(None)):
    if not urlpath or not timestamp or not nonce:
        return BaseResponse(msg="Params Error, need 3 params: urlpath timestamp nonce", success=False)

    if len(nonce) != 32:
        return BaseResponse(msg="Params Error, nonce must be 32", success=False)
    if not Matcher.match(nonce):
        return BaseResponse(msg="Params Error, nonce invalid", success=False)

    try:
        tm = int(timestamp)
    except Exception:
        return BaseResponse(msg="Params Error, timestamp invalid", success=False)

    if not urlpath.endswith("/"):
        urlpath += "/"

    result = enc1(urlpath=urlpath, timecasp=tm, nonce=nonce)

    return Response(content=result)

@app.get("/encode2")
@app.post("/encode2")
async def encode2(urlpath: str = Query(None), timestamp: str = Query(None), nonce: str = Query(None)):
    if not urlpath or not timestamp or not nonce:
        return BaseResponse(msg="Params Error, need 3 params: urlpath timestamp nonce", success=False)

    if len(nonce) != 32:
        return BaseResponse(msg="Params Error, nonce must be 32", success=False)
    if not Matcher.match(nonce):
        return BaseResponse(msg="Params Error, nonce invalid", success=False)

    try:
        tm = int(timestamp)
    except Exception:
        return BaseResponse(msg="Params Error, timestamp invalid", success=False)

    if not urlpath.endswith("/"):
        urlpath += "/"

    result = enc2(urlpath=urlpath, timecasp=tm, nonce=nonce)

    return Response(content=result)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=9000)
