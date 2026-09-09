# ******************************************************************************
#  Unlicensed. Free for usage without warranty, expressed or implied
#
#  Implementation of Conway's Game of Life
#
#  Filename   : Game_protocol.py
#  Description:
#    This Python program implements a simple zero-player game similar to
#    Conway's Game of Life (CGoL). CGoL was devised by John Horton Conway in
#    1970.  https://en.wikipedia.org/wiki/Conway's_Game_of_Life
#
#    This game is similar, but it uses a hexagonal grid rather than the
#    square grid used in CGoL. The rules are similar, but the reproduction and
#    overpopulation counts are configurable.
#
#    This file implements the class Game as an abstract protocol class.
#    All methods and properties of this class are virtual.
#
#  Change log:
#    2026-09-09  KSM  Created
#
#  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
# ******************************************************************************

from CellArray import CellArraySize, CellArrayPos, ResizeAnchor
from typing import Protocol, Self
import numpy.typing as npt
import re

type Designator = tuple[int, int, str]|None
type GameSpec = tuple[str, int, int, bool, str]
type GamesList = list[GameSpec]
type ValueTypes = bool|int
type RuleSpec = tuple[set[int], set[int]]
type Rules = str


class Game(Protocol):

    def __init__(self, obj:Self|None=None, rules:Rules="B3/S23") -> None:
        ...

    @property
    def rules(self) -> Rules:
        ...

    @rules.setter
    def rules(self, rules:Rules):
        ...

    def new_game(self, *, size:CellArraySize, name:str="", is_warp:bool=True) -> Designator:
        ...

    def load_pattern(self, pattern:str, *, name:str="", size:CellArraySize=(0,0), is_warp:bool=True) -> Designator:
        ...

    def load_preset(self, preset:int) -> Designator:
        ...

    def load_file(self, filename:str) -> Designator:
        ...

    def set_snapshot(self, snapshot:str) -> bool:
        ...

    def get_snapshot(self) -> str:
        ...

    def save_file(self, filename:str, *, name:str="") -> bool:
        ...

    @property
    def designator(self) -> Designator:
        ...

    @property
    def games_list(self) -> GamesList:
        ...

    @property
    def games_names_list(self) -> list[str]:
        ...

    def grid_data(self) -> npt.NDArray:
        ...

    @property
    def size(self) -> CellArraySize:
        ...

    @property
    def rows(self) -> int:
        ...

    @property
    def cols(self) -> int:
        ...

    @property
    def name(self) -> str:
        ...

    @property
    def live_cells(self) -> int:
        ...

    @property
    def is_warp(self) -> bool:
        ...

    @is_warp.setter
    def is_warp(self, warp:bool) -> None:
        ...

    def clear(self, size:CellArraySize) -> None:
        ...

    def resize(self, size:CellArraySize, *, anchor:ResizeAnchor="nw") -> None:
        ...

    def advance_generation(self) -> int:
        ...

    def __str__(self) -> str:
        ...

    def __getitem__(self, pos:CellArrayPos) -> ValueTypes:
        ...

    def __setitem__(self, pos:CellArrayPos, value:ValueTypes) -> None:
        ...


    # non-protocol utility function
    @staticmethod
    def _decode_rules(rules:Rules) -> RuleSpec:
        """Decode cellular automaton rules in B/S form

        Args:
            rules: [str]    ex/ "B3/S23"  (see notes)

        Returns:
            [tuple[set,set]]   (birth_set, survival_set)

        Notes:
            The "B/S" syntax is commonly used for cellular automaton games.
            B is followed by one or more digits. Each digit represents a number
            of cells. If a dead cell has a neighboring cell count matching one
            of those numbers in the birth set, then it becomes a living cell.
            S is followed by one or more digits. Each digit represents a number
            of cells. If a live cell has a neighboring cell count matching one
            of those numbers in the survival set, then it survies otherwise it
            dies.
        """
        if m := re.match(r"\s*B\s*([1-9]+)\s*/\s*S\s*([0-9]+)\s*$", rules, re.IGNORECASE):
            set_b = set()
            set_s = set()
            for c in m.group(1):
                set_b.add(int(c))
            for c in m.group(2):
                set_s.add(int(c))
        else:
            # default rules = standard CGoL rules B3/S23
            set_b = { 3 }
            set_s = { 2, 3 }
        return (set_b, set_s)


    @staticmethod
    def _encode_rules(spec:RuleSpec) -> Rules:
        """Encode cellular automaton rules in B/S form

        Args:
            spec:  [tuple[set,set]]   (birth_set, survival_set)

        Returns:
            [str]  rules in "B/S" form

        Notes:
            The "B/S" syntax is commonly used for cellular automaton games.
            B is followed by one or more digits. Each digit represents a number
            of cells. If a dead cell has a neighboring cell count matching one
            of those numbers in the birth set, then it becomes a living cell.
            S is followed by one or more digits. Each digit represents a number
            of cells. If a live cell has a neighboring cell count matching one
            of those numbers in the survival set, then it survies otherwise it
            dies.
        """
        set_b = spec[0]
        set_s = spec[1]
        code_b = [ str(c) for c in sorted(set_b)]
        code_s = [ str(c) for c in sorted(set_s)]
        return f"B{code_b}/S{code_s}"


# ******************************************************************************
#  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
#  Unlicensed. Free for usage without warranty, expressed or implied
# ******************************************************************************