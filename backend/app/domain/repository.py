from abc import ABC, abstractmethod
from typing import List, Optional
from .models import User

class UserRepository(ABC):
    @abstractmethod
    def get_user(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def list_users(self) -> List[User]:
        pass
