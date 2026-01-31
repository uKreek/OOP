from event_class import CoffeeClubMember, MukbangEnjoyer, Validator, Logger, LenValidator

validator1 = Validator()
logger = Logger()

name_len_validator = LenValidator('name', 18)
food_len_validator = LenValidator('favorite_food', 4)

Vladislav = CoffeeClubMember('Vladislav', 'coffee', 'potato')

Vladislav.property_changing += validator1
Vladislav.property_changed += logger

Vladislav.name = 'Sergey'
Vladislav.favorite_drink = 'still_water'
Vladislav.favorite_food = 'peace'

Santana = MukbangEnjoyer('Santana', 'NikocadoAvocado', 'pasta')

Santana.property_changing += name_len_validator
Santana.property_changing += food_len_validator

Vladislav.property_changed += logger

Santana.name = 'asdfghjklqwertyuiopfghj'
Santana.favorite_blogger = 'Lololowka'
Santana.favorite_food = 'burger'
