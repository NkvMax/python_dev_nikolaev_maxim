from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
import io
import csv

from app.domain.use_cases.comments_use_case import get_comments_for_user

router = APIRouter()


@router.get("/")
def get_comments(login: str = Query(...), format: str = Query("json")):
    """
    Эндпоинт для получения датасета comments по логину пользователя, с выбором формата выдачи JSON/CSV
    \nПример:
        - GET /api/comments?login=john | Если не указать формат то выдаст JSON
        - GET api/comments?login=john&format=csv | С указанием формата JSON/CSV
    """
    data = get_comments_for_user(login)

    if format.lower() == "csv":
        # Генерируем CSV как строку
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["user_login", "post_header", "post_author_login", "total_comments"])
        for row in data:
            writer.writerow([
                row["user_login"],
                row["post_header"],
                row["post_author_login"],
                row["total_comments"],
            ])
        csv_content = output.getvalue()
        output.close()

        # Создаем StreamingResponse
        response = StreamingResponse(
            iter([csv_content]),
            media_type="text/csv"
        )
        # Заставляем браузер (или другой клиент) скачивать файл как "comments.csv"
        response.headers["Content-Disposition"] = "attachment; filename=comments.csv"
        return response

    # По умолчанию JSON
    return {
        "status": "ok",
        "data": data
    }
