from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic

TEventArgs = TypeVar('TEventArgs')
T = TypeVar('T')


class EventHandler(ABC, Generic[TEventArgs]):
    @abstractmethod
    def handle(self, sender: Any, args: TEventArgs) -> None:
        pass


class Event(Generic[TEventArgs]):
    def __init__(self):
        self._handlers = []

    def __iadd__(self, handler: EventHandler) -> TEventArgs:
        self._handlers.append(handler)
        return self

    def __isub__(self, handler: EventHandler) -> TEventArgs:
        if handler in self._handlers:
            self._handlers.remove(handler)
        return self

    def __call__(self, sender: T, args: TEventArgs):
        for h in self._handlers:
            h.handle(self, args)


class EventArgs:
    pass


class PropertyChangedEventArgs(EventArgs):
    def __init__(self, property_name: str):
        self.property_name = property_name


class Logger(EventHandler[PropertyChangedEventArgs]):
    def handle(self, sender: Any, args: TEventArgs) -> None:
        print(f'object {sender} changed property {args.property_name}')


class PropertyChangingEventArgs(EventArgs):
    def __init__(self, property_name: str, old_value: Any, new_value: Any):
        self.property_name = property_name
        self.old_value = old_value
        self.new_value = new_value
        self.can_change = True


class LenValidator(EventHandler[PropertyChangingEventArgs]):
    def __init__(self, property_name: str, value_len: int):
        self.value_len = value_len
        self.property_name = property_name

    def handle(self, sender: Any, args: TEventArgs) -> None:
        if len(str(args.new_value)) > self.value_len and args.property_name == self.property_name:
            print(f'ERROR: the value of {self.property_name} is too long. The allowed length is: {self.value_len}')
            args.can_change = False


class Validator(EventHandler[PropertyChangingEventArgs]):
    def handle(self, sender: Any, args: TEventArgs) -> None:
        print(f'object {sender} try to change property {args.property_name} from {args.old_value} to {args.new_value}')

        if args.new_value == '':
            print(f'ERROR: this field cannot be empty')
            args.can_change = False

        if args.property_name == 'favorite_drink' and args.new_value != 'coffee':
            print(f'ERROR: this is a coffee fans club')
            args.can_change = False

        if args.property_name == 'favorite_food' and args.new_value == 'peace':
            print('EROOR: GET OUT!')
            args.can_change = False


class CoffeeClubMember:
    def __init__(self, name: str, favorite_drink: str, favorite_food: str):
        self._name = name
        self._favorite_food = favorite_food
        self._favorite_drink = favorite_drink

        self.property_changed = Event[PropertyChangedEventArgs]()
        self.property_changing = Event[PropertyChangingEventArgs]()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        if self._name == value:
            return

        args_changing = PropertyChangingEventArgs('name', self._name, value)
        self.property_changing(self, args_changing)

        if not args_changing.can_change:
            return

        self._name = value
        self.property_changed(self, PropertyChangedEventArgs('name'))

    @property
    def favorite_drink(self):
        return self._favorite_drink

    @favorite_drink.setter
    def favorite_drink(self, value: str):
        if self._favorite_drink == value:
            return

        args_changing = PropertyChangingEventArgs('favorite_drink', self._favorite_drink, value)
        self.property_changing(self, args_changing)

        if not args_changing.can_change:
            return

        self._favorite_drink = value
        self.property_changed(self, PropertyChangedEventArgs('favorite_drink'))

    @property
    def favorite_food(self):
        return self._favorite_food

    @favorite_food.setter
    def favorite_food(self, value: str):
        if self._favorite_food == value:
            return

        args_changing = PropertyChangingEventArgs('favorite_food', self._favorite_food, value)
        self.property_changing(self, args_changing)

        if not args_changing.can_change:
            return

        self._favorite_food = value
        self.property_changed(self, PropertyChangedEventArgs('favorite_food'))


class MukbangEnjoyer:
    def __init__(self, name: str, favorite_blogger: str, favorite_food: str):
        self._name = name
        self._favorite_blogger = favorite_blogger
        self.favorite_drink = favorite_food

        self.property_changed = Event[PropertyChangedEventArgs]()
        self.property_changing = Event[PropertyChangingEventArgs]()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        if self._name == value:
            return

        args_changing = PropertyChangingEventArgs('name', self._name, value)
        self.property_changing(self, args_changing)

        if not args_changing.can_change:
            return




















































































































































































































































































































































































































































































































































        self._name = value
        self.property_changed(self, PropertyChangedEventArgs('name'))

    @property
    def favorite_blogger(self):
        return self

    @favorite_blogger.setter
    def favorite_blogger(self, value: str):
        if self._name == value:
            return

        args_changing = PropertyChangingEventArgs('favorite_blogger', self._name, value)
        self.property_changing(self, args_changing)

        if not args_changing.can_change:
            return

        self._name = value
        self.property_changed(self, PropertyChangedEventArgs('favorite_blogger'))

    @property
    def favorite_food(self):
        return self

    @favorite_food.setter
    def favorite_food(self, value: str):
        if self._name == value:
            return

        args_changing = PropertyChangingEventArgs('favorite_food', self._name, value)
        self.property_changing(self, args_changing)

        if not args_changing.can_change:
            return
        self._name = value
        self.property_changed(self, PropertyChangedEventArgs('favorite_food'))
