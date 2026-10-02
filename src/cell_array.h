/*******************************************************************************
*  Unlicensed. Free for usage without warranty, expressed or implied
*
*  Implementation of Conway's Game of Life
*
*  Filename   : cell_array.h
*  Description:
*    This C++ program implements a simple zero-player game known as
*    Conway's Game of Life (CGoL). CGoL was devised by John Horton Conway in
*    1970.  https://en.wikipedia.org/wiki/Conway's_Game_of_Life
*
*    This file contains the interface for the CellArray, the class that holds
*    a 2D grid of bool cells.
*
*  Change log:
*    2026-09-22  KSM  Created
*
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
* ******************************************************************************/

#pragma once

#include "app_config.h"
#include <cstdint>


/// @brief array anchor enumeration (NW, N, NE, W, X, E, SW, S, SE)
enum array_anchor_t
{
    X  = 0,
    NW = 1,
    N  = 2,
    NE = 3,
    W  = 4,
    E  = 5,
    SW = 6,
    S  = 7,
    SE = 8
};
using ANCHOR = array_anchor_t;


/// @brief a 2D array of bool cells
class CellArray
{
protected:
    array_shape_t m_shape;
    size_t m_allocated_size;
    bool* m_data;

public:
    // --- construction, destruction, copying, and assignment ---
    CellArray(array_shape_t shape=array_shape_t::NONE, bool value=false) noexcept;
    CellArray(CellArray const& src) noexcept;
    CellArray(CGOL_STRING const& src);
    CellArray& operator = (CellArray const& src) noexcept;
    CellArray& operator = (CGOL_STRING const& src);
    virtual ~CellArray() noexcept;

    // --- manipulation ---
    void clear(bool value=false) noexcept;
    void resize(array_shape_t shape, array_anchor_t anchor=ANCHOR::X);

    // --- element access ---
    bool& operator () (int row, int col) noexcept;
    const bool& operator () (int row, int col) const noexcept;
    bool& operator [] (array_index_t pos) noexcept;
    const bool& operator [] (array_index_t pos) const noexcept;

    // --- properties ---

    /// @brief retrieve the CellArray shape
    /// @return shape {rows, cols}; {0,0} for an empty CellArray
    array_shape_t shape() const noexcept
    {
        return m_shape;
    }

    /// @brief retrieve the number of CellArray rows
    /// @return number of rows; 0 for an empty CellArray
    int rows() const noexcept
    {
        return m_shape.rows;
    }

    /// @brief retrieve the number of CellArray columns
    /// @return number of columns; 0 for an empty CellArray
    int cols() const noexcept
    {
        return m_shape.cols;
    }

    /// @brief determine if the CellArray is non-empty (true) or empty (false)
    explicit operator bool() const noexcept
    {
        return bool(m_shape);
    }

    size_t live_count() const noexcept;

    /// @brief retrieve the total number of cells in the CellArray
    /// @return number of cells in CellArray; 0 for an empty CellArray
    size_t cell_count() const noexcept
    {
        return (m_shape.rows* m_shape.cols);
    }

    // --- I/O functions ---
    CGOL_STRING toString() const noexcept;
    void fromString(CGOL_STRING const& src);

private:
    void raw_copy_from(CellArray const& src) noexcept;
    void raw_set_value(bool value) noexcept;
    void coerce_coordinate(int& row, int& col) const noexcept;
};


/*******************************************************************************
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
*  Unlicensed. Free for usage without warranty, expressed or implied
********************************************************************************/