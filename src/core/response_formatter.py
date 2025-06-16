from fastapi.responses import JSONResponse


class ApiResponseFormatter:
    @staticmethod
    def success(**data):
        return JSONResponse(
            content=data,
            status_code=200,
        )
