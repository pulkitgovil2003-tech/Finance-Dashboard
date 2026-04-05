from fastapi.responses import JSONResponse



def success_response(message: str, data=None):
    return {
        "status": "SUCCESS",
        "message": message,
        "data": data
    }


def failure_response(message: str, data=None):
    return JSONResponse(
        status_code=400,
        content={
            "status": "FAILURE",
            "message": message,
            "data": data
        }
    )
    