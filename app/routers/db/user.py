from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends

from app.db.models import User
from app.schemas.user import SearchUser, UserIn, UserOut

router = APIRouter()


def write_log(user: str, message=""):
    with open("log.txt", mode="a") as log_file:
        content = f"{user} {message}\n"
        log_file.write(content)


@router.get("/say-hi", response_model=UserOut)
async def hello_world(
    edad: int,
    user_in: UserOut = Depends(UserOut),
    nombre: str = None,
):
    """
    # este endopoint retorna un hola mundo
    **jhoty** : es un muchachon de Dios

    """
    user = UserOut(name=nombre, age=edad)
    return user


@router.post("/", response_model=UserOut)
async def create_user(back_task: BackgroundTasks, user_in: UserIn):
    usuario = await User.create(
        name=user_in.name, age=user_in.age, is_active=user_in.is_active
    )
    back_task.add_task(write_log, usuario.name, "se creo el usuario")

    return usuario


@router.get("/get-all", response_model=List[UserOut])
async def get_all_users(
    user_filter: SearchUser = Depends(SearchUser), limit: int = 10, offset: int = 0
):
    return (
        await User.filter(**user_filter.dict(exclude_none=True))
        .all()
        .limit(limit)
        .offset(offset)
    )


@router.get(
    "/{user_id}",
    response_model=UserOut,
    responses={200: {"detail": "User founded"}, 404: {"detail": "User not found"}},
)
async def get_user_by_id(user_id: int):
    return await User.get(id=user_id)


@router.delete("/{user_id}", responses={204: {}})
async def delete_user(user_id: int):
    await User.filter(id=user_id).first().delete()