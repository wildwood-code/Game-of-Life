/*******************************************************************************
*  Unlicensed. Free for usage without warranty, expressed or implied
*
*  Implementation of Conway's Game of Life
*
*  Filename   : cgol_types.h
*  Description:
*    This C++ program implements a simple zero-player game known as
*    Conway's Game of Life (CGoL). CGoL was devised by John Horton Conway in
*    1970.  https://en.wikipedia.org/wiki/Conway's_Game_of_Life
*
*    This file contains declarations of types used throughout the game.
*
*  Change log:
*    2026-09-21  KSM  Created
*    2026-09-24  KSM  Moved standard types and preset games into this file
*
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
* ******************************************************************************/

#pragma once

#include <vector>
#include <set>

//#define USE_STANDARD_TYPES  // for development only
#ifdef USE_STANDARD_TYPES
    #include <string>
    using CGOL_STRING = std::string;
    using CGOL_CHAR  = char;
    #define CGOL_FORMAT(...) std::format(__VA_ARGS__)
    #define CGOL_EMPTY_STRING ""
#else
    #include <wx/string.h>
    using CGOL_STRING = wxString;
    using CGOL_CHAR = wxUniChar;
    #define CGOL_FORMAT(...) wxString::Format(__VA_ARGS__)
    #define CGOL_EMPTY_STRING wxEmptyString
#endif


/// @brief rules description string in B/S format: ex/ "B3/S23"
using Rules = CGOL_STRING;

/// @brief grid pattern string: ex/ "x.x;.xx;.x."
using Pattern = CGOL_STRING;

/// @brief game designator structure
/// @param rows
/// @param cols
/// @param name
struct Designator
{
    int rows;
    int cols;
    CGOL_STRING name;

    operator bool() const noexcept
    {
        return rows>0 && cols>0;
    }

    static const Designator INVALID;
};

inline const Designator Designator::INVALID{0,0,""};

/// @brief full game specification structure
/// @param name
/// @param rows
/// @param cols
/// @param is_warp
/// @param rules
/// @param anchor [int] 0=ctr, 1=NW, 2=N, 3=NE, 4=W, 5=E, 6=SW, 7=S, 8=SE
/// @param pattern
struct GameSpec
{
    CGOL_STRING name;
    int rows;
    int cols;
    bool is_warp;
    Rules rules;
    int anchor;
    Pattern pattern;
};

/// @brief vector containing zero or more GameSpec structures
using GamesList = std::vector<GameSpec>;

/// @brief vector containing a list of all preset and registered games
using GamesNamesList = std::vector<CGOL_STRING>;

/// @brief a "tuple" struct containing sets for birth and survive rules
struct RuleSpec
{
    std::set<int> birth;
    std::set<int> survive;

    RuleSpec copy() const
    {
        RuleSpec tgt;
        tgt.birth = birth;
        tgt.survive = survive;

        return tgt;
    }
};

/// @brief vector containing a list of all unique B/S encoded rules
using RulesList = std::vector<Rules>;

struct HeadEntry
{
    int r;
    int c;
};

/// @brief object to hold an entry in the "insert structure" context menu
/// @note Pattern entry:     { "name", "pattern", {r,c} };
/// @note Non-pattern entry: { "label", "", {-1,val} };
/// @note Separator entry:   { "",      "", {-1,-1} }
struct StructureSpec
{
    CGOL_STRING name;
    CGOL_STRING pattern;
    HeadEntry head;

    explicit operator bool() const noexcept
    {
        return !name.empty();
    }

    static const StructureSpec NONE;
    static const StructureSpec SEPARATOR;
    static const StructureSpec LABEL(const CGOL_STRING& label, int value);
    static const StructureSpec PATTERN(const CGOL_STRING& name, const CGOL_STRING& pattern, HeadEntry head);
};

inline const StructureSpec StructureSpec::NONE{"", "", {-1,-1}};
inline const StructureSpec StructureSpec::SEPARATOR{"", "", {-1,-1}};
inline const StructureSpec StructureSpec::LABEL(const CGOL_STRING& label, int value)
{
    return StructureSpec(label, "", {-1,value});
}
inline const StructureSpec StructureSpec::PATTERN(const CGOL_STRING& name, const CGOL_STRING& pattern, HeadEntry head)
{
    return StructureSpec(name, pattern, head);
}

/// @brief vector containing a list of StructureSpec entries
using StructureList = std::vector<StructureSpec>;


/// @brief array shape "tuple" {rows, cols}
struct array_shape_t
{
    int rows;
    int cols;

    /// @brief determine if the array with this shape is not empty (true) or empty (false)
    explicit operator bool () const noexcept
    {
        return rows>0 && cols>0;
    }

    /// @brief  determine if the array with this smape is empty
    /// @return true if empty; false if not empty
    bool empty() const noexcept
    {
        return rows<=0 || cols<=0;
    }

    /// @brief determines if an index r,c is within our bounds
    /// @return true if r,c is within bounds; false if it is not within bounds
    bool inside(int r, int c) const noexcept
    {
        return r>=0 && r<rows && c>=0 && c<cols;
    }

    /// @brief determine if an index r,c is outside of our bounds
    /// @return true if r,c is not within bounds; false if it is within bounds
    bool outside(int r, int c) const noexcept
    {
        return r<0 || r>=rows || c<0 || c>=cols;
    }

    static const array_shape_t NONE;
};

inline const array_shape_t array_shape_t::NONE{0, 0};


/// @brief array index "tuple" {row, col}
struct array_index_t
{
    int r;
    int c;

    /// @brief comparison operator for two indices
    /// @return true if they are equal; false if they are not equal
    bool operator == (const array_index_t& obj) const noexcept
    {
        return r == obj.r && c == obj.c;
    }

    /// @brief determine if the array index is defined (true) or none (false)
    explicit operator bool () const noexcept
    {
        return r >= 0 && c >= 0;
    }

    /// @brief is the index inside the given array shape?
    bool inside(const array_shape_t& shape) const noexcept
    {
        return 0<=r && r<shape.rows && 0<=c && c<shape.cols;
    }

    /// @brief is the index outside the given array shape?
    bool outside(const array_shape_t& shape) const noexcept
    {
        return r<0 || r>=shape.rows || c<0 || c>=shape.cols;
    }

    static const array_index_t INVALID;
};

inline const array_index_t array_index_t::INVALID{-1, -1};


/*******************************************************************************
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
*  Unlicensed. Free for usage without warranty, expressed or implied
********************************************************************************/