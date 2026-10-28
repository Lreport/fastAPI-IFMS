"""Recebe as requisicoes HTTP e chama as operacoes do model."""

from typing import Annotated

from fastapi import APIRouter, Form, HTTPException, Path, Query, Response, status

from models import activity as activity_model
from models.activity import ActivityInput, ActivityOutput, Subject


router = APIRouter(prefix="/activities", tags=["Activities"])


@router.post(
    "",
    response_model=ActivityOutput,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar uma atividade",
)
async def create_activity(data: Annotated[ActivityInput, Form()]) -> dict:
    """Recebe o formulario e cadastra uma atividade.

    Args:
        data (ActivityInput): Dados validados recebidos nos campos do formulario.

    Returns:
        dict: Atividade cadastrada, usada no corpo da resposta HTTP 201.
    """
    return activity_model.create(data)


@router.get(
    "",
    response_model=list[ActivityOutput],
    summary="Listar atividades",
)
async def list_activities(
    subject: Annotated[
        Subject | None, Query(description="Filtrar pelo nome completo da disciplina.")
    ] = None,
    done: Annotated[
        bool | None, Query(description="Filtrar atividades concluidas ou pendentes.")
    ] = None,
) -> list[dict]:
    """Consulta as atividades com filtros opcionais.

    Args:
        subject (Subject | None, optional): Disciplina usada no filtro.
            None inclui todas as disciplinas. Padrao: None.
        done (bool | None, optional): True inclui concluidas e False inclui
            pendentes. None inclui ambas. Padrao: None.

    Returns:
        list[dict]: Lista de atividades que correspondem aos filtros.
    """
    return activity_model.get_all(subject, done)


@router.get(
    "/{activity_id}",
    response_model=ActivityOutput,
    summary="Consultar uma atividade",
    responses={404: {"description": "Atividade nao encontrada."}},
)
async def get_activity(
    activity_id: Annotated[int, Path(gt=0, description="ID da atividade.")],
) -> dict:
    """Consulta uma atividade pelo identificador.

    Args:
        activity_id (int): Identificador positivo recebido no caminho da requisicao.

    Raises:
        HTTPException: Erro HTTP 404 quando a atividade nao existe.

    Returns:
        dict: Dados da atividade encontrada.
    """
    activity = activity_model.get_by_id(activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Atividade nao encontrada.")
    return activity


@router.put(
    "/{activity_id}",
    response_model=ActivityOutput,
    summary="Substituir os dados de uma atividade",
    responses={404: {"description": "Atividade nao encontrada."}},
)
async def update_activity(
    activity_id: Annotated[int, Path(gt=0, description="ID da atividade.")],
    data: Annotated[ActivityInput, Form()],
) -> dict:
    """Substitui os dados de uma atividade existente.

    Args:
        activity_id (int): Identificador positivo da atividade que sera atualizada.
        data (ActivityInput): Novos dados. Campos opcionais omitidos usam
            description=None e done=False.

    Raises:
        HTTPException: Erro HTTP 404 quando a atividade nao existe.

    Returns:
        dict: Atividade atualizada com o mesmo identificador.
    """
    activity = activity_model.update(activity_id, data)
    if activity is None:
        raise HTTPException(status_code=404, detail="Atividade nao encontrada.")
    return activity


@router.delete(
    "/{activity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    summary="Excluir uma atividade",
    responses={404: {"description": "Atividade nao encontrada."}},
)
async def delete_activity(
    activity_id: Annotated[int, Path(gt=0, description="ID da atividade.")],
) -> Response:
    """Exclui uma atividade pelo identificador.

    Args:
        activity_id (int): Identificador positivo da atividade que sera removida.

    Raises:
        HTTPException: Erro HTTP 404 quando a atividade nao existe.

    Returns:
        Response: Resposta HTTP 204 sem corpo.
    """
    if not activity_model.delete(activity_id):
        raise HTTPException(status_code=404, detail="Atividade nao encontrada.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
