# ******************************************************************************
#  Unlicensed. Free for usage without warranty, expressed or implied
#
#  Implementation of Conway's Game of Life
#
#  Filename   : CellArray.py
#  Description:
#    This Python program implements a simple zero-player game similar to
#    Conway's Game of Life (CGoL). CGoL was devised by John Horton Conway in
#    1970.  https://en.wikipedia.org/wiki/Conway's_Game_of_Life
#
#    This game is similar, but it uses a hexagonal grid rather than the
#    square grid used in CGoL. The rules are similar, but the reproduction and
#    overpopulation counts are configurable.
#
#    This file implements the CellArray[T] class, which is a generic scalar
#    array (bool, int, float), extended with a few useful functions.
#
#  Change log:
#    2026-09-09  KSM  Created
#
#  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
# ******************************************************************************

import numpy as np
import numpy.typing as npt
from typing import Literal
from collections.abc import Callable
import re
from static_init import static_init

type CellArraySize = tuple[int, int]
type CellArrayPos  = tuple[int, int]
type ResizeAnchor  = Literal["x", "nw", "n", "ne", "w", "e", "sw", "s", "se"]


def func_default_translation_int(val:int|str) -> str|int:
    """Translation function: int <-> str

    Args:
        val: [int]  Translate int value 0..9 into '0'..'9'
             [str]  Translate str value '0'..'9' into 0..9

    Returns:
        [str]  '0'..'9' if val was an int
        [int]  0..9     if val was a str
    """
    if isinstance(val, str):
        # default translation: str -> int
        return ord(val[0])-ord('0')
    else:
        # default translation: int -> str
        return chr(val+ord('0'))


def func_default_translation_bool(val:bool|str) -> str|bool:
    if isinstance(val, str):
        # default translation: str -> int
        return False if val[0]=='.' else True
    else:
        # default translation: int -> str
        return "#" if val else "."


def func_default_translation_float(val:float|str) -> str|float:
    if isinstance(val, str):
        # default translation: str -> int
        return 0.0 if val[0]=='.' else 1.0
    else:
        # default translation: int -> str
        return "#" if val else "."


@static_init
class CellArray[T]:

    @classmethod
    def static_init(cls):
        # regular expressions
        cls.RE_PARSE_GRID = re.compile(r"^(.+)$", re.MULTILINE)


    def __init__(self, obj:"CellArray|str|None"=None, *, size:CellArraySize=(0,0), dtype:type[T]|None=None, func:Callable[[T|str],str|T]|None = None):
        """CellArray[T] constructor

        Args:
            obj:
            size:
            dtype:
            fntran:

        Raises:
            TypeError: _description_
            ValueError: _description_

        Notes:
            The translation function has two forms:
                func(val:T) -> str
                func(val:str) -> T

            It either translates a value to a single-charactor or it translates a
            single-character to a value.

            An example protype would be:
                func_int_trans(int|str) -> str|int

            See func_default_translation_int() above for an example of a
            translation function.
        """

        rows, cols = size

        self._translate : Callable[[T|str],str|T]|None = func

        if isinstance(obj, CellArray):
            self._nr : int = obj._nr
            self._nc : int = obj._nc
            self._dtype : type = obj._dtype
            self._data : npt.NDArray = obj._data.copy()
            if dtype is not None and dtype != self._dtype:
                raise TypeError(f"dtype={dtype.__name__} is not compatible with obj being copied.")
        else:
            self._nr : int = 0
            self._nc : int = 0
            self._dtype : type = dtype if dtype is not None else bool
            self._data : npt.NDArray = np.zeros((0,0), dtype=self._dtype)
            if isinstance(obj, str):
                # lines are separated by newlines
                # translation function is called to map str -> val
                success = False
                m = CellArray.RE_PARSE_GRID.findall(obj)
                while m is not None: # if-loop with break out
                    nr = len(m)
                    if not nr > 0: break
                    nc = len(m[0])
                    if not nc > 0: break
                    self._nr = nr
                    self._nc = nc
                    self._data = np.zeros((nr, nc), dtype=self._dtype)
                    for i in range(nr):
                        row = m[i]
                        if not len(row) == nc: break
                        for j in range(nc):
                            val = self.__translate(row[j])
                            self._data[i,j] = val
                    success = True
                    break

                if not success:
                    raise ValueError("Invalid init string")

        if rows != self._nr or cols != self._nc:
            self.resize(size=(rows, cols), anchor="x")


    def __translate(self, val:T|str) -> str|T:
        if self._translate is not None:
            return self._translate(val)
        elif self._dtype == bool:
            return func_default_translation_bool(val) # type: ignore
        elif self._dtype == int:
            return func_default_translation_int(val) # type: ignore
        else:
            return func_default_translation_float(val) # type: ignore


    def __bool__(self) -> bool:
        """Grid test: is it non-zero-dimension?

        Returns:
            False if the grid is 0x0 dimension; True otherwise
        """
        return self._nr > 0 and self._nc > 0


    def clear(self):
        """Clear the grid: make all cells the null-value for the dtype
        """
        self._data.fill(self._dtype())


    def copy(self) -> "CellArray":
        """Clone the grid: make a copy of itself

        Returns:
            Returns a new Grid object that is a copy of this one.
        """
        my_clone = CellArray(self)
        return my_clone


    @property
    def size(self) -> CellArraySize:
        """Grid dimensions: recalls the size (rows, cols) of the grid as a tuple

        Returns:
            Tuple (rows, cols)
        """
        return (self._nr, self._nc)


    @property
    def live_count(self) -> int:
        """Grid property: number of non-null grid cells

        Returns:
            Number of non-null grid cells

        Note:
            A non-null cell is any cell that does not evaluate to True
        """
        live = 0
        for i in range(self._nr):
            for j in range(self._nc):
                if self._data[i, j]: live += 1
        return live


    @property
    def cell_count(self) -> int:
        """Grid property: number of cells in the grid

        Returns:
            Number of cells in the grid, including True/live and False/dead
        """
        return self._nr * self._nc


    @property
    def rows(self) -> int:
        """Grid property: number of rows in the grid

        Returns:
            Number of rows in the grid
        """
        return self._nr


    @property
    def cols(self) -> int:
        """Grid property: number of columns in the grid

        Returns:
            Number of columns in the grid
        """
        return self._nc


    def _coerce(self, pos:CellArrayPos) -> CellArrayPos:
        """Coerce the given grid position (r,c) into one within the warped grid

        Args:
            pos: [tuple] Grid position: (r, c)

        Returns:
            [tuple] Coerced grid position: (r, c)
                    (-1, -1) for a 0x0 grid
        """
        r, c = pos
        r = r % self._nr if self._nr != 0 else -1
        c = c % self._nc if self._nc != 0 else -1
        return (r, c)


    def __getitem__(self, pos:CellArrayPos) -> T:
        """Grid indexing: obj[r, c]

        Args:
            pos: [tuple] Position in the grid as a tuple (r, c)

        Returns:
            Grid state True/False at the given position
        """
        r, c = self._coerce(pos)
        return self._data[r, c]


    def __setitem__(self, pos:CellArrayPos, value:T):
        """Grid indexing: obj[r, c] = value

        Args:
            pos:   [tuple] Position in the grid: (r, c)
            value: [T] Grid state to set the given position
        """
        r, c = self._coerce(pos)
        self._data[r, c] = value


    def data_copy(self) -> npt.NDArray:
        """Get a copy of the raw Numpy array

        Returns:
            Copy of raw Numpy array
        """
        return self._data.copy()


    def resize(self, size:CellArraySize, *, anchor:ResizeAnchor="nw"):
        """Resize the Grid object

        Args:
            rows:   [int] Target number of rows {default 0}
            cols:   [int] Target number of cols {default 0}
                          0 => don't change rows/cols; + => target rows/cols
            anchor: Anchor position {default "nw"}
                    ["nw", "n", "ne", "w", "x", "e", "sw", "s", "se"]
        """
        rows, cols = size
        if rows > 0:
            my_rows, my_cols = self.size
            rows_t = 0  # number of top rows to add or subtract
            rows_b = 0  # number of bottom rows to add or subtract
            add_rows = rows - my_rows

            match anchor:
                case "x" | "w" | "e":
                    # divide equally (favor bottom if odd)
                    rows_t = int(add_rows/2)
                    rows_b = add_rows - rows_t

                case "nw" | "n" | "ne":
                    # add/subtract at bottom
                    rows_b = add_rows

                case "sw" | "s" | "se":
                    # add/subtract at top
                    rows_t = add_rows

            if add_rows > 0:
                data = np.vstack((np.zeros((rows_t, my_cols), dtype=self._dtype), self._data, np.zeros((rows_b, my_cols), dtype=self._dtype)))
                self._data = data
                self._nr = rows

            elif add_rows < 0:
                rows_delete = np.r_[0:-rows_t, my_rows+rows_b:my_rows]
                data = np.delete(self._data, rows_delete, axis=0)
                self._data = data
                self._nr = rows

        if cols > 0:
            my_rows, my_cols = self.size
            cols_l = 0  # number of left cols to add or subtract
            cols_r = 0  # number of right cols to add or subtract
            add_cols = cols - my_cols

            match anchor:
                case "x" | "n" | "s":
                    # divide equally (favor right)
                    cols_l = int(add_cols/2)
                    cols_r = add_cols - cols_l

                case "nw" | "w" | "sw":
                    # add/subtract at right
                    cols_r = add_cols

                case "ne" | "e" | "se":
                    # add/subtract at left
                    cols_l = add_cols

            if add_cols > 0:
                data = np.hstack((np.zeros((my_rows, cols_l), dtype=self._dtype), self._data, np.zeros((my_rows, cols_r), dtype=self._dtype)))
                self._data = data
                self._nc = cols

            elif add_cols < 0:
                cols_delete = np.r_[0:-cols_l, my_cols+cols_r:my_cols]
                data = np.delete(self._data, cols_delete, axis=1)
                self._data = data
                self._nc = cols


    def __repr__(self) -> str:
        """Grid representation (partial)

        Returns:
            Displays the grid representation partially. By partially, the size
            is shown and the number of live cells, but not the grid data.
        """
        n_live = self.live_count
        return f"Grid(rows={self._nr}, cols={self._nc}, live_cells={n_live})"


    def __str__(self) -> str:
        """Grid data as a string

        Returns:
            Returns a string with newlines splitting rows. The number of chars
            on each row is the number of columns. The chars used to represent
            live and dead cells is specified in the Grid static variables.
        """
        grid = ""
        for i in range(self._nr):
            row = ""
            for j in range(self._nc):
                val = self._data[i,j]
                e :str  = self.__translate(val) # type: ignore
                row = row + e
            grid = grid + row
            if i < self._nr-1:
                grid = grid + "\n"
        return grid


if __name__ == "__main__":

    def my_trans(val:int|str) -> str|int:
        pass
        if isinstance(val, str):
            my_val = ord(val[0])-ord('0')
            return my_val
        else:
            ch = chr(val+ord('0'))
            return ch

    v = CellArray("315\n605\n122\n498", dtype=int, size=(8,10))

    print(str(v))
    print(v._data)
    v.resize(size=(6,6), anchor="x")
    print(v._data)

    u = CellArray("..xx\n.xx.\nx..x\nx.x.\n.x.x", size=(6,6), dtype=bool)
    print(u._data)
    print(str(u))


# ******************************************************************************
#  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
#  Unlicensed. Free for usage without warranty, expressed or implied
# ******************************************************************************