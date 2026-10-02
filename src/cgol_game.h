/*******************************************************************************
*  Unlicensed. Free for usage without warranty, expressed or implied
*
*  Implementation of Conway's Game of Life
*
*  Filename   : cgol_game.h
*  Description:
*    This C++ program implements a simple zero-player game known as
*    Conway's Game of Life (CGoL). CGoL was devised by John Horton Conway in
*    1970.  https://en.wikipedia.org/wiki/Conway's_Game_of_Life
*
*    This file contains the interface for the CGOL game engine.
*
*  Change log:
*    2026-09-22  KSM  Created
*
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
* ******************************************************************************/

#pragma once

#include "app_config.h"
#include "cell_array.h"


#define DEFAULT_RULES  "B3/S23"

class CGOL_Game
{
protected:
    Designator m_designator;
    CellArray  m_grid;
    size_t     m_live_cell_count;
    bool       m_is_warp;
    GamesList  m_registered_games;
    RuleSpec   m_rule_spec;

public:
    // --- construction, destruction, and copying ---

    CGOL_Game(Rules rules=DEFAULT_RULES);
    CGOL_Game(CGOL_Game const& obj);
    ~CGOL_Game() = default;

    // --- loading, saving, and new game creation ---

    const Designator& new_game(array_shape_t shape, CGOL_STRING const& name=CGOL_EMPTY_STRING, bool is_warp=true);
    const Designator& load_pattern(Pattern pattern, CGOL_STRING const& name=CGOL_EMPTY_STRING, bool is_warp=true, array_shape_t shape=array_shape_t::NONE, Rules rules=DEFAULT_RULES);
    const Designator& load_preset(int preset);
    const Designator& load_file(CGOL_STRING const& filename);
    bool save_file(CGOL_STRING const& filename, CGOL_STRING const& name=CGOL_EMPTY_STRING);

    // --- game progression ---

    size_t advance_generation();

    // --- game information lists ---

    GamesNamesList get_games_names_list() const noexcept;
    RulesList get_rules_list() const noexcept;

    // --- snapshots ---

    bool set_snapshot(CGOL_STRING const& snapshot);
    CGOL_STRING get_snapshot(CGOL_STRING name=CGOL_EMPTY_STRING) const;

    // --- game properties ---

    /// @brief Get the rules for the CGOL_Game object
    /// @return game rules in B/S form (e.g., "B3/S23")
    Rules get_rules() const  { return encode_rules(m_rule_spec); }

    /// @brief Set the rules for a CGOL_Game object
    /// @param rules game rules in B/S form (e.g., "B3/S23")
    void set_rules(Rules const& rules)  { m_rule_spec = decode_rules(rules); }

    void get_rule_spec(RuleSpec& spec) const { spec = m_rule_spec.copy(); }
    void set_rule_spec(RuleSpec const& spec) { m_rule_spec = spec; }


    const Designator& get_designator() const  { return m_designator; }

    CellArray get_grid_data() const  { return CellArray(m_grid); }

    array_shape_t get_shape() const  { return m_grid.shape(); }

    int get_rows() const  { return m_grid.rows(); }

    int get_cols() const  { return m_grid.cols(); }

    CGOL_STRING get_name() const  { return m_designator.name; }
    void set_name(CGOL_STRING const& name) { m_designator.name = name; }

    size_t get_live_cell_count() const { return m_live_cell_count; }
    void refresh_live_cell_count() { m_live_cell_count = m_grid.live_count(); }

    bool is_warp() const  { return m_is_warp; }

    void set_warp(bool warp)  { m_is_warp = warp; }

    void register_game();

    // --- game grid manipulation ---

    void clear();
    void resize(array_shape_t shape, array_anchor_t anchor=ANCHOR::NW);
    void add_pattern_at(const Pattern& pattern, const array_index_t& pos);

    // --- game information: string representations ---

    CGOL_STRING toString(CGOL_STRING name="") const;
    CGOL_STRING toGridString() const;

    // --- game grid indexing ---

    const bool& operator() (int row, int col) const;
    bool& operator() (int row, int col);

protected:
    static void rules_warp_at_edge(const CellArray& grid_now, CellArray& grid_next, const RuleSpec& rules, size_t& live_cells);
    static void disintegrate_at_edge(CellArray& grid, size_t& live_cells);
    static RuleSpec decode_rules(Rules const& rules);
    static Rules encode_rules(RuleSpec const& spec);

protected:
    static const Designator s_invalid_designator;
};



/*******************************************************************************
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
*  Unlicensed. Free for usage without warranty, expressed or implied
********************************************************************************/