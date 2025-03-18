from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
import io
import csv
from app.domain.use_cases.general_use_case import get_general_for_user

router = APIRouter()


@router.get("/")
def get_general(login: str = Query(...), format: str = Query("json")):
    """
    Эндпоинт для получения общего датасета general по логину пользователя, с выбором формата выдачи JSON/CSV
    \nПример:
        - GET /api/general?login=john | Если не указать формат то выдаст JSON
        - GET /api/general?login=natalya&format=csv | С указанием формата JSON/CSV
    """
    data = get_general_for_user(login)

    if format.lower() == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["date", "logins", "logouts", "blog_actions"])
        for row in data:
            writer.writerow([
                row["date"],
                row["logins"],
                row["logouts"],
                row["blog_actions"],
            ])
        csv_content = output.getvalue()
        output.close()

        response = StreamingResponse(
            iter([csv_content]),
            media_type="text/csv"
        )
        response.headers["Content-Disposition"] = "attachment; filename=general.csv"
        return response

    return {
        "status": "ok",
        "data": data
    }

