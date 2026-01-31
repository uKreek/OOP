from abc import ABC, abstractmethod
from typing import List, Dict


class ICommand(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass


class Keyboard:
    def __init__(self):
        self.keys: Dict[str, ICommand] = {}
        self._history: List[str] = []
        self._redo_stack: List[str] = []
        self.text_buffer: List[str] = []

    def bind(self, hot_keys: str, command: ICommand) -> None:
        self.keys[hot_keys] = command

    def press(self, hot_keys: str):
        if hot_keys in self.keys:
            ...



class VolumeUpCommand(ICommand):
    def execute(self) -> None:
        print('Volume increased +10%')

    def undo(self) -> None:
        print('Volume decreased -10%')


class VolumeDownCommand(ICommand):
        def execute(self) -> None:
            print('Volume decreased -10%')

        def undo(self) -> None:
            print('Volume increased +10%')


class MediaPlayerCommand(ICommand):
    def execute(self) -> None:
        print('Media player launched')

    def undo(self) -> None:
        print('Media player closed')


class KeybordStateSaver(ICommand)   :
    ...
