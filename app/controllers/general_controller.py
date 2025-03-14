from fastapi import APIRouter, Query
from app.domain.use_cases.general_use_case import get_general_for_user

router = APIRouter()


@router.get("/")
def get_general(login: str = Query(...)):
    """
    Эндпоинт для получения общего датасета general по логину пользователя
    Пример: GET /api/general?login=john
    """
    data = get_general_for_user(login)
    return {
        "status": "ok",
        "data": data
    }
