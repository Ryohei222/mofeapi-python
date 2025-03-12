from dataclasses import dataclass

from mofeapi.enums import PublicStatus

# TODO: createdAt, updatedAt は datetime に変更する


@dataclass
class Post:
    id: int
    title: str
    content: str
    public_status: PublicStatus
    created_at: str
    updated_at: str
