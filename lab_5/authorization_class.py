from typing import TypeVar, Union, Generic, Sequence, List, Protocol, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod
import os
import pickle


class HasID(Protocol):
    data_id: int


T = TypeVar('T', bound=HasID)


@dataclass
class User:
    data_id: int
    name: str
    login: str
    password: str
    email: Union[str, None] = None
    address: Union[str, None] = None

    def __repr__(self):
        return f'User({self.data_id = }, {self.name = }, {self.login = }, {self.email = }, {self.address = })'

    def __lt__(self, other):
        return self.name < other.name

# region Interfaces


class IDataRepository(ABC, Generic[T]):
    @abstractmethod
    def get_all(self) -> Sequence[T]:
        pass

    @abstractmethod
    def get_by_id(self, data_id: int) -> Union[T, None]:
        pass

    @abstractmethod
    def add(self, item: T) -> None:
        pass

    @abstractmethod
    def update(self, item: T) -> None:
        pass

    @abstractmethod
    def delete(self, item: T) -> None:
        pass


class IUserRepository(IDataRepository[User]):
    @abstractmethod
    def get_by_login(self, login: str) -> Union[User, None]:
        pass


class IAuthService(ABC):
    @abstractmethod
    def sign_in(self, user: User) -> None:
        pass

    @abstractmethod
    def sign_out(self, user: User) -> None:
        pass

    @abstractmethod
    def is_authorized(self) -> bool:
        pass

    @abstractmethod
    def current_user(self) -> User:
        pass

# endregion


class DataRepository(IDataRepository[T]):
    def __init__(self, file_name: str):
        self._file_name = file_name
        self._items: List[T] = []

    def _load(self) -> list[T]:
        if not os.path.exists(self._file_name):
            return []
        try:
            with open(self._file_name, "rb") as f:
                return pickle.load(f)
        except Exception:
            return []

    def _save(self) -> None:
        with open(self._file_name, "wb") as f:
            pickle.dump(self._items, f)

    def get_all(self) -> Sequence[T]:
        return sorted(self._items)

    def get_by_id(self, data_id: int) -> Union[T, None]:
        for item in self._items:
            if item.data_id == data_id:
                return item
        return None

    def add(self, item: T) -> None:
        self._items.append(item)
        self._save()

    def update(self, item: T) -> None:
        target_id = item.data_id
        for i, existing_item in enumerate(self._items):
            if existing_item.data_id == target_id:
                self._items[i] = item
                self._save()
                return

    def delete(self, item: T) -> None:
        target_id = item.data_id
        for i in self._items:
            if i.data_id == target_id:
                self._items.remove(i)


class UserRepository(DataRepository[User], IUserRepository):
    def get_by_login(self, login: str) -> Union[User, None]:
        for user in self._items:
            if user.login == login:
                return user
        return None


class AuthService(IAuthService):
    def __init__(self, user_repo: UserRepository, session_file: str = 'session.pkl'):
        self._repo = user_repo
        self._session_file = session_file
        self._current_user: Optional[User] = None
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self._session_file):
            self._current_user = None
            return
        try:
            with open(self._session_file, "rb") as f:
                self._current_user = pickle.load(f)
        except Exception:
            self._current_user = None

    def _save(self) -> None:
        if self._current_user is None:
            if os.path.exists(self._session_file):
                os.remove(self._session_file)
        else:
            with open(self._session_file, "wb") as f:
                pickle.dump(self._current_user, f)

    def sign_in(self, user: User) -> None:
        self._current_user = user
        self._save()

    def sign_out(self, user: User) -> None:
        if self._current_user and self._current_user.data_id == user.data_id:
            self._current_user = None
            self._save()

    def is_authorized(self) -> bool:
        return self._current_user is not None

    @property
    def current_user(self) -> User:
        return self._current_user
