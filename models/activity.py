"""Define as disciplinas, os dados de entrada e saida e as operacoes em memoria."""

from enum import Enum
from itertools import count

from pydantic import BaseModel, ConfigDict, Field


class Subject(str, Enum):
    """Lista as disciplinas aceitas no cadastro."""

    APIS_AND_MICROSERVICES = "APIs e Microserviços"
    INTELLIGENT_AGENTS = "Agentes Inteligentes"
    EXTENSION_IV = "Atividade de Extensão IV"
    ASYNC_COMMUNICATION_AND_OBSERVABILITY = "Comunicação Assíncrona e Observabilidade"
    BACK_END_FRAMEWORKS = "Frameworks Back-End"
    STATISTICS = "Fundamentos de Estatística"
    PROJECT_MANAGEMENT = "Gestão de Projetos"


class ActivityInput(BaseModel):
    """Valida os dados enviados no cadastro e na atualizacao."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    title: str = Field(min_length=1, max_length=100, description="Titulo da atividade.")
    subject: Subject = Field(description="Disciplina da atividade.")
    description: str | None = Field(
        default=None, max_length=500, description="Detalhes opcionais da atividade."
    )
    done: bool = Field(default=False, description="Indica se a atividade foi concluida.")


class ActivityOutput(ActivityInput):
    """Inclui o ID gerado pela API nos dados de saida."""

    id: int = Field(gt=0, description="Identificador gerado pela API.")


activities: dict[int, dict] = {}
next_id = count(1)


def create(data: ActivityInput) -> dict:
    """Cria uma atividade na memoria e gera seu identificador.

    Args:
        data (ActivityInput): Dados validados da nova atividade.

    Returns:
        dict: Atividade criada com o identificador gerado.
    """
    activity = {"id": next(next_id), **data.model_dump()}
    activities[activity["id"]] = activity
    return activity


def get_all(subject: Subject | None = None, done: bool | None = None) -> list[dict]:
    """Lista as atividades e aplica os filtros informados.

    Args:
        subject (Subject | None, optional): Disciplina usada no filtro.
            None inclui todas as disciplinas. Padrao: None.
        done (bool | None, optional): True inclui concluidas e False inclui
            pendentes. None inclui ambas. Padrao: None.

    Returns:
        list[dict]: Atividades que correspondem aos filtros, ou uma lista vazia.
    """
    result = list(activities.values())
    if subject is not None:
        result = [activity for activity in result if activity["subject"] == subject]
    if done is not None:
        result = [activity for activity in result if activity["done"] == done]
    return result


def get_by_id(activity_id: int) -> dict | None:
    """Busca uma atividade pelo identificador.

    Args:
        activity_id (int): Identificador da atividade procurada.

    Returns:
        dict | None: Atividade encontrada, ou None quando o identificador nao existe.
    """
    return activities.get(activity_id)


def update(activity_id: int, data: ActivityInput) -> dict | None:
    """Substitui os dados de uma atividade e mantem seu identificador.

    Args:
        activity_id (int): Identificador da atividade que sera atualizada.
        data (ActivityInput): Novos dados. Campos opcionais omitidos usam
            description=None e done=False.

    Returns:
        dict | None: Atividade atualizada, ou None quando o identificador nao existe.
    """
    if activity_id not in activities:
        return None
    activity = {"id": activity_id, **data.model_dump()}
    activities[activity_id] = activity
    return activity


def delete(activity_id: int) -> bool:
    """Remove uma atividade da memoria.

    Args:
        activity_id (int): Identificador da atividade que sera removida.

    Returns:
        bool: True quando a atividade foi removida, ou False quando nao existe.
    """
    return activities.pop(activity_id, None) is not None
