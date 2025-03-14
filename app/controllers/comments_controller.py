from fastapi import APIRouter, Query
from app.domain.use_cases.comments_use_case import get_comments_for_user

router = APIRouter()


@router.get("/")
def get_comments(login: str = Query(...)):
    """
    Эндпоинт для получения датасета comments по логину пользователя
    Пример: GET /api/comments?login=john
    """
    data = get_comments_for_user(login)
    return {
        "status": "ok",
        "data": data
    }
