from fastapi.responses import JSONResponse


def badresponse(msg):
    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "message": f"Error in request data. {msg}"
            },
    )
