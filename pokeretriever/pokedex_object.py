import abc


class PokedexObject(abc.ABC):
    """
    A representation of a pokedex.
    """

    @abc.abstractmethod
    def __init__(self, name, id):
        self._name = name
        self._id = id

    @abc.abstractmethod
    def __str__(self):
        return f"Name: {self._name}\n" \
               f"ID: {self._id}"


class Ability(PokedexObject):
    """
    A representation of an ability
    """
    def __init__(self, name: str, id: int, generation: str, effect: str, short_effect: str, pokemon: list):
        super().__init__(name, id)
        self._generation = generation
        self._effect = effect
        self._short_effect = short_effect
        self._pokemon = pokemon

    def __str__(self):
        return f"Ability {super().__str__()}\n" \
               f"Generation: {self._generation}\n" \
               f"Effect: {self._effect}\n" \
               f"Effect(Short): {self._short_effect}\n" \
               f"Pokemon list: {', '.join(self._pokemon)}\n"


class Stat(PokedexObject):
    """
    A representation of a stat.
    """

    def __init__(self, name: str, id: int, base_stat: int, is_battle_only: bool):
        super().__init__(name, id)
        self._base_stat = base_stat
        self._is_battle_only = is_battle_only

    def __str__(self):
        return f"Stat {super().__str__()}\n" \
               f"Base stat: {self._base_stat}\n" \
               f"Battle only: {self._is_battle_only}\n"


class Move(PokedexObject):
    """
    A representation of a move.
    """

    def __init__(self, name: str, id: int, generation: str, accuracy: int, pp: int,
                 power: int, move_type: str, damage_class: str, short_effect: str):
        super().__init__(name, id)
        self._generation = generation
        self._accuracy = accuracy
        self._pp = pp
        self._power = power
        self._move_type = move_type
        self._damage_class = damage_class
        self._short_effect = short_effect

    def __str__(self):
        return f"Move {super().__str__()}\n" \
               f"Generation: {self._generation}\n" \
               f"Accuracy: {self._accuracy}\n" \
               f"PP: {self._pp}\n" \
               f"Power: {self._power}\n" \
               f"Move type: {self._move_type}\n" \
               f"Damage class: {self._damage_class}\n" \
               f"Effect(Short): {self._short_effect}\n"


class Pokemon(PokedexObject):
    """
    A representation of a pokemon.
    """

    def __init__(self, name: str, id: int, height: int, weight: int, stats: list,
                 types: list, abilities: list, moves: list, isExpanded: bool):
        super().__init__(name, id)
        self._height = height
        self._weight = weight
        self._stats = stats
        self._types = types
        self._abilities = abilities
        self._moves = moves
        self._isExpanded = isExpanded

    def __str__(self):
        nl = '\n'
        if self._isExpanded:
            return f"Pokemon {super().__str__()}\n" \
                   f"Height: {self._height}\n" \
                   f"Weight: {self._weight}\n" \
                   f"\n*****Stats***** \n\n{nl.join([stat.__str__() for stat in self._stats])}\n" \
                   f"Types: {', '.join(self._types)}\n" \
                   f"\n*****Abilities***** \n\n{nl.join([ability.__str__() for ability in self._abilities])}\n" \
                   f"\n*****Moves***** \n\n{nl.join([move.__str__() for move in self._moves])}"
        else:
            return f"Pokemon {super().__str__()}\n" \
                   f"Height: {self._height}\n" \
                   f"Weight: {self._weight}\n" \
                   f"Types: {', '.join(self._types)}\n" \
