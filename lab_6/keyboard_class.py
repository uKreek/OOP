from abc import ABC, abstractmethod
from typing import List, Dict, Any
import json
import os


class VirtualOS:
    def __init__(self):
        self.text_buffer: List[str] = []

    def add_char(self, char: str):
        return self.text_buffer.append(char)

    def remove_char(self):
        if self.text_buffer:
            return self.text_buffer.pop()
        return


CLASS_REGISTRY = {}


def class_registry(cls):
    CLASS_REGISTRY[cls.__name__] = cls
    return cls


class ICommand(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, os_obj: VirtualOS, data: Dict) -> object:
        pass


class Keyboard:
    def __init__(self, os_obj: VirtualOS):
        self.os_obj = os_obj
        self.keys: Dict[str, ICommand] = {}
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


@class_registry
class KeyCommand(ICommand):
    def __init__(self, os_obj: VirtualOS, char: str):
        self.os_obj = os_obj
        self.char = char

    def execute(self) -> None:
        self.os_obj.add_char(self.char)
        print(''.join(self.char))

    def undo(self) -> None:
        self.os_obj.remove_char()
        print(''.join(self.char))

    def to_dict(self) -> Dict[str, str]:
        return {'char': self.char}

    @classmethod
    def from_dict(cls, os_obj: VirtualOS, data: Dict) -> object:
        return cls(os_obj, data['char'])


@class_registry
class VolumeUpCommand(ICommand):
    def __init__(self, os_obj: VirtualOS):
        self.os_obj = os_obj

    def execute(self) -> None:
        print('Volume increased +10%')

    def undo(self) -> None:
        print('Volume decreased -10%')

    def to_dict(self) -> Dict[str, None]:
        return {}

    @classmethod
    def from_dict(cls, os_obj: VirtualOS, data: Dict) -> object:
        return cls(os_obj)


@class_registry
class VolumeDownCommand(ICommand):
    def __init__(self, os_obj: VirtualOS):
        self.os_obj = os_obj

    def execute(self) -> None:
        print('Volume decreased -10%')

    def undo(self) -> None:
        print('Volume increased +10%')

    def to_dict(self) -> Dict[str, None]:
        return {}

    @classmethod
    def from_dict(cls, os_obj: VirtualOS, data: Dict) -> object:
        return cls(os_obj)


@class_registry
class MediaPlayerCommand(ICommand):
    def __init__(self, os_obj: VirtualOS):
        self.os_obj = os_obj

    def execute(self) -> None:
        print('Media player launched')

    def undo(self) -> None:
        print('Media player closed')

    def to_dict(self) -> Dict[str, None]:
        return {}

    @classmethod
    def from_dict(cls, os_obj: VirtualOS, data: Dict) -> object:
        return cls(os_obj)


class Mapper:
    @staticmethod
    def map_to_dict(keys_dict: Dict[str, ICommand]) -> Dict[str, Dict[str, Dict[str, str]]]:
        data = {}
        for key_combo, command in keys_dict.items():
            cmd_class = type(command).__name__
            data[key_combo] = {
                'cmd_class': cmd_class,
                'args': command.to_dict()
            }
        return data

    @staticmethod
    def map_from_dict(data: Dict[str, Any], os_obj: VirtualOS) -> Dict[str, ICommand]:
        restored_keys = {}
        for key_combo, info in data.items():
            cls_name = info.get('cmd_class', {})
            args = info.get('args', {})
            cmd_class = CLASS_REGISTRY.get(cls_name)
            if cmd_class:
                command = cmd_class.from_dict(os_obj, args)
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

        new_keys = Mapper.map_from_dict(data_dict, keyboard.os_obj)
        keyboard.keys = new_keys
        return True
