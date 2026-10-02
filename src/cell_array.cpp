/*******************************************************************************
*  Unlicensed. Free for usage without warranty, expressed or implied
*
*  Implementation of Conway's Game of Life
*
*  Filename   : cell_array.cpp
*  Description:
*    This C++ program implements a simple zero-player game known as
*    Conway's Game of Life (CGoL). CGoL was devised by John Horton Conway in
*    1970.  https://en.wikipedia.org/wiki/Conway's_Game_of_Life
*
*    This file implements CellArray, the class that holds a 2D grid of
*    bool cells.
*
*  Change log:
*    2026-09-21  KSM  Created
*
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
* ******************************************************************************/

#include "cell_array.h"
#include <stdexcept>


/// @brief CellArray constructor
/// @param shape shape of the empty array. {rows, cols}: default={0,0} -> empty
/// @param value initialization value: default=false
CellArray::CellArray(array_shape_t shape, bool value) noexcept
: m_data(nullptr), m_allocated_size(0), m_shape(array_shape_t::NONE)
{
    if (shape)
    {   // allocate array
        m_shape = shape;
        m_allocated_size = shape.rows * shape.cols;
        m_data = new bool[m_allocated_size];
        raw_set_value(value);
    }
    else
    {   // allocate one dummy element for indexing access
        m_allocated_size = 1;
        m_data = new bool[m_allocated_size];
    }
}


/// @brief Raw copy from source array to target array (this)
/// @param src The non-empty source array
/// @note  No checking is performed.
///        Use only on an empty target and non-empty src.
//         Use: delete[] m_data PRIOR to calling raw_copy_from()
void CellArray::raw_copy_from(CellArray const& src) noexcept
{
    m_shape = src.m_shape;
    m_allocated_size = src.m_allocated_size;
    m_data = new bool[m_allocated_size];
    for (auto i=0; i<m_allocated_size; ++i)
        m_data[i] = src.m_data[i];
}


/// @brief Raw setting of the value of each element of the target array (this)
/// @param value Value to set. default=false.
/// @note  No checking is performed.
///        Use only on an allocated (non-empty) target.
void CellArray::raw_set_value(bool value) noexcept
{
    for (auto i=0; i<m_allocated_size; ++i)
        m_data[i] = value;
}


/// @brief CellArray copy constructor
/// @param src source array for copy
CellArray::CellArray(CellArray const& src) noexcept
: m_data(nullptr), m_allocated_size(0), m_shape(array_shape_t{0,0})
{
    raw_copy_from(src);
}


/// @brief CellArray constructor from a descriptor string
/// @param src cell array descriptor string
/// @note descriptor string is one row per line; separators are semicolon or newline
/// '.' for a dead cell, 'x' for a live cell
CellArray::CellArray(CGOL_STRING const& src)
: m_data(nullptr), m_allocated_size(0), m_shape(array_shape_t{0,0})
{
    fromString(src);
}


/// @brief CellArray assignment operator
/// @param src source array for assignment
/// @return *this array reference
CellArray& CellArray::operator = (CellArray const& src) noexcept
{
    delete[] m_data;
    raw_copy_from(src);
    return *this;
}


/// @brief CellArray assignment operator
/// @param src cell array descriptor string
/// @note descriptor string is one row per line; separators are semicolon or newline
/// '.' for a dead cell, 'x' for a live cell
/// @return *this array reference
CellArray& CellArray::operator = (CGOL_STRING const& src)
{
    fromString(src);
    return *this;
}


/// @brief CellArray destructor
CellArray::~CellArray()
{
    delete[] m_data;
}


/// @brief Clear entire array (or set it to the given value)
/// @param value optional value to set (true, false)  default = false
void CellArray::clear(bool value) noexcept
{
    if (m_shape)
        raw_set_value(value);
}


/// @brief Resize the array to the given shape with the given anchor
/// @param shape new shape of the array {rows, cols}
/// @param anchor [ANCHOR] for resize (NW, N, NE, W, X, E, SW, S, SE) default=X
void CellArray::resize(array_shape_t shape, array_anchor_t anchor)
{
    // create a new, empty, reshaped array of the target shape
    CellArray reshaped(shape);

    if (reshaped && m_shape)  // both reshaped and this array are non-empty
    {   // copy the new array in where it intersects
        // start by identifying where it is anchored
        int r_offs, c_offs;  // row, col offset where *this(0,0) will intersect

        switch (anchor)
        {
            case NW: case N: case NE:
                r_offs = 0;
                break;

            case W: case X: case E:
                // use (. / 2) to round down (-5 / 2) == -3
                // use (. >> 1) to round towards zero (-5 >> 1) == -2
                r_offs = (reshaped.m_shape.rows - m_shape.rows) >> 1;
                break;

            case SW: case S: case SE:
                r_offs = reshaped.m_shape.rows - m_shape.rows;
                break;
        }

        switch (anchor)
        {
            case NW: case W: case SW:
                c_offs = 0;
                break;

            case N: case X: case S:
                // use (. / 2) to round down (-5 / 2) == -3
                // use (. >> 1) to round towards zero (-5 >> 1) == -2
                c_offs = (reshaped.m_shape.cols - m_shape.cols) >> 1;
                break;

            case NE: case E: case SE:
                c_offs = reshaped.m_shape.cols - m_shape.cols;
                break;
        }

        // now, copy element-by-element where there is intersection
        for (auto r=0; r<m_shape.rows; ++r)
        {   for (auto c=0; c<m_shape.cols; ++c)
            {
                int xr = r + r_offs;
                int xc = c + c_offs;

                if ( xr<0 || xr>=reshaped.m_shape.rows || xc<0 || xc>=reshaped.m_shape.cols )
                    continue;

                reshaped(xr, xc) = this->operator() (r, c);
            }
        }
    }

    // finally, copy the reshaped array over our existing array
    *this = reshaped;
}


/// @brief Indexed write operator:  array(row,col) = value
/// @param row 0-based row index
/// @param col 0-based column index
/// @return writeable reference to the indexed cell
/// @note  throws out_of_range exception if index is out-of-range
bool& CellArray::operator () (int row, int col) noexcept
{
    coerce_coordinate(row, col);
    size_t idx = row*m_shape.cols + col;
    return m_data[idx];
}


/// @brief Indexed write operator: array[{row,col}] = value
/// @param pos 0-based position {row, col}
/// @return writeable reference to the indexed cell
/// @note  throws out_of_range exception if index is out-of-range
bool& CellArray::operator [] (array_index_t pos) noexcept
{
    int row = pos.r, col = pos.c;
    coerce_coordinate(row, col);
    size_t idx = row*m_shape.cols + col;
    return m_data[idx];
}


/// @brief Indexed read operator: value = array(row, col)
/// @param row 0-based row index
/// @param col 0-based column index
/// @return non-writeable reference to the indexed cell
/// @note  throws out_of_range exception if index is out-of-range
const bool& CellArray::operator () (int row, int col) const noexcept
{
    coerce_coordinate(row, col);
    size_t idx = row*m_shape.cols + col;
    return m_data[idx];
}


/// @brief Indexed read operator: value = array[{row,col}]
/// @param pos 0-based position {row, col}
/// @return non-writeable reference to the indexed cell
/// @note  throws out_of_range exception if index is out-of-range
const bool& CellArray::operator [] (array_index_t pos) const noexcept
{
    int row = pos.r, col = pos.c;
    coerce_coordinate(row, col);
    size_t idx = row*m_shape.cols + col;
    return m_data[idx];
}


/// @brief Returns count of "live" cells in the array
/// @return count of cells that evaulate to true ("live")
size_t CellArray::live_count() const noexcept
{
    size_t count = 0;

    if (m_shape)
    {   for (auto i=0; i<m_allocated_size; ++i)
            if (m_data[i])  count += 1;
    }

    return count;
}


/// @brief Convert the cell array to a string type
/// @return '.' for dead/false cells, 'x' for live/true cells;
/// empty string "" if the cell array is empty
/// @note Generates one row per line with a newline after each row
CGOL_STRING CellArray::toString() const noexcept
{
    CGOL_STRING result;

    if (m_shape)
    {   for (auto r=0; r<m_shape.rows; ++r)
        {   for (auto c=0; c<m_shape.cols; ++c)
            {
                if (this->operator()(r, c))
                    result += "x";
                else
                    result += ".";
            }
            result += "\n";
        }
    }
    else
    {
        result = "<empty>";
    }

    return result;
}


/// @brief Convert the array descriptor string into an array
/// @param src cell array descriptor string
/// @note descriptor string is one row per line; separators are semicolon or newline
/// '.' for a dead cell, 'x' for a live cell
void CellArray::fromString(CGOL_STRING const& src)
{
    if (!src.empty())
    {
        int cols = -1;  // intentional -1 is used here
        int rows = 0;
        int r = 0, c = 0;
        bool is_line = false;

        // first pass, just validate character contents and determine size
        for (auto ch : src)
        {
            is_line = false;
            switch (char(ch))
            {
                case ';': case ':': case '\n':
                    // line break
                    is_line = true;
                    break;

                case '.': case ' ': case '-':
                case 'x': case 'X': case '#': case '%': case '+':
                    break;

                default:
                    throw std::invalid_argument("Invalid character in descriptor string");
            }

            if (is_line)
            {
                if (cols == -1)
                {   // first row is done
                    if (c == 0)
                        throw std::invalid_argument("Invalid 0-column size in descriptor string");
                    cols = c;
                }
                else if (c != cols)
                {
                    throw std::invalid_argument("Inconsistent column length i descriptor string");
                }

                rows += 1;
                c = 0;
            }
            else
            {
                c += 1;
            }
        }

        if (!is_line)
        {
            // termination was not a line-break, so do our sizing checks now
            rows += 1;
            if (cols == -1)
            {
                if (c == 0)
                    throw std::invalid_argument("Invalid 0-column size in descriptor string");
                cols = c;
            }
            else if (c != cols)
            {
                throw std::invalid_argument("Inconsistent column length i descriptor string");
            }
        }

        if (rows==0)
            throw std::invalid_argument("Invalid 0-row size in descriptor string");

        // second pass, read the actual data
        resize({rows, cols});
        r = 0;
        c = 0;
        for (auto ch : src)
        {
            bool cell = false;
            is_line = false;

            switch (char(ch))
            {
                case ';': case ':': case '\n':
                    // line break
                    is_line = true;
                    break;

                case '.': case ' ': case '-':
                    // dead cell
                    cell = false;
                    break;

                case 'x': case 'X': case '#': case '%': case '+':
                    // live cell
                    cell = true;
                    break;
            }

            if (is_line)
            {
                r += 1;
                c = 0;
            }
            else
            {
                operator() (r, c) = cell;
                c += 1;
            }
        }
    }
    else
    {   // empty string -> empty CellArray
        resize(array_shape_t::NONE);
    }
}


/// @brief Optimized integer modulo function with correct behavior for negative value
/// @param k  integer being calculated
/// @param n  modulo base
/// @return   true mod(k, n)
inline int int_mod(int k, int n) noexcept
{
    return (0 <= k && k < n) ? k : (k < 0 ? k % n + n : k % n);
}


/// @brief Function to coerce the coordinates to warp at edges
/// @param row 0-based row index
/// @param col 0-based column index
void CellArray::coerce_coordinate(int& row, int& col) const noexcept
{
    row = int_mod(row, m_shape.rows);
    col = int_mod(col, m_shape.cols);
}


/*******************************************************************************
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
*  Unlicensed. Free for usage without warranty, expressed or implied
********************************************************************************/