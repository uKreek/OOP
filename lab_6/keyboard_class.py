from abc import ABC, abstractmethod
from typing import List, Dict, Any
import json
import os


class ICommand(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass

    @abstractmethod
    def get_params(self) -> Dict:
        pass


class Keyboard:
    def __init__(self):
        self.keys: Dict[str, ICommand] = {}
        self.text_buffer: List[str] = []
        self._history: List[ICommand] = []
        self._redo_stack: List[ICommand] = []

    def bind(self, key_combo: str, command: ICommand) -> None:
        self.keys[key_combo] = command

    def press(self, key_combo: str) -> None:
        if key_combo in self.keys:
            command = self.keys[key_combo]
            command.execute()

            self._history.append(command)
            self._redo_stack.clear()
        else:
            print('Command is not define')

    def undo(self) -> None:
        if self._history:
            command = self._history.pop()
            command.undo()
            self._redo_stack.append(command)

    def redo(self) -> None:
        if self._redo_stack:
            command = self._redo_stack.pop()
            command.execute()

            self._history.append(command)


class KeyCommand(ICommand):
    def __init__(self, buffer: List, char: str):
        self.buffer = buffer
        self.char = char

    def execute(self) -> None:
        self.buffer.append(self.char)
        print(''.join(self.buffer))

    def undo(self) -> None:
        if self.buffer:
            self.buffer.pop()
            print(''.join(self.buffer))

    def get_params(self) -> Dict:
        return {'char': self.char}


class VolumeUpCommand(ICommand):
    def execute(self) -> None:
        print('Volume increased +10%')

    def undo(self) -> None:
        print('Volume decreased -10%')

    def get_params(self) -> Dict:
        return {}


class VolumeDownCommand(ICommand):
        def execute(self) -> None:
            print('Volume decreased -10%')

        def undo(self) -> None:
            print('Volume increased +10%')

        def get_params(self) -> Dict:
            return {}


class MediaPlayerCommand(ICommand):
    def execute(self) -> None:
        print('Media player launched')

    def undo(self) -> None:
        print('Media player closed')

    def get_params(self) -> Dict:
        return {}


CLASS_REGISTRY = {
    'KeyCommand': KeyCommand,
    'VolumeUpCommand': VolumeUpCommand,
    'VolumeDownCommand': VolumeDownCommand,
    'MediaPlayerCommand': MediaPlayerCommand
}


class Mapper:
    @staticmethod
    def map_to_dict(keys_dict: Dict[str, ICommand]) -> Dict:
        data = {}
        for key_combo, command in keys_dict.items():
            cmd_class = type(command).__name__
            data[key_combo] = {
                'cmd_class': cmd_class,
                'args': command.get_params()
            }
        return data

    @staticmethod
    def map_from_dict(data: Dict[str, Any], buffer: List[str]) -> Dict:
        restored_keys = {}
        for key_combo, info in data.items():
            cls_name = info.get('cmd_class', {})
            args = info.get('args', {})
            cmd_class = CLASS_REGISTRY.get(cls_name)
            if cmd_class:
                if cls_name == 'KeyCommand':
                    command = cmd_class(buffer, **args)
                else:
                    command = cmd_class(**args)
                restored_keys[key_combo] = command

        return restored_keys


class Serializer:
    @staticmethod
    def serialize(filename: str, data: Dict):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def deserialize(filename: str) -> Dict:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)


class KeyboardStateSaver:
    def __init__(self, filename: str):
        self.filename = filename

    def save_state(self, keyboard: Keyboard):
        data_dict = Mapper.map_to_dict(keyboard.keys)
        Serializer.serialize(self.filename, data_dict)

    def restore_state(self, keyboard: Keyboard) -> bool:
        if not os.path.exists(self.filename):
            return False
        data_dict = Serializer.deserialize(self.filename)

        new_keys = Mapper.map_from_dict(data_dict, keyboard.text_buffer)
        keyboard.keys = new_keys
        return True
