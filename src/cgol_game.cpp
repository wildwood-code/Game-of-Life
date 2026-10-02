/*******************************************************************************
*  Unlicensed. Free for usage without warranty, expressed or implied
*
*  Implementation of Conway's Game of Life
*
*  Filename   : cgol_game.cpp
*  Description:
*    This C++ program implements a simple zero-player game known as
*    Conway's Game of Life (CGoL). CGoL was devised by John Horton Conway in
*    1970.  https://en.wikipedia.org/wiki/Conway's_Game_of_Life
*
*    This file contains the implementation of the CGOL game engine.
*
*  Change log:
*    2026-09-22  KSM  Created
*
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
* ******************************************************************************/

#include "app_config.h"
#include "cgol_game.h"
#include <wx/tokenzr.h>
#include <wx/filename.h>
#include <format>
#include <algorithm>
#include <fstream>
#include <sstream>
#include <unordered_set>
#include <queue>


/// @brief CGOL_Game constructor
/// @param rules game rules in B/S form; default = "B3/S23"
CGOL_Game::CGOL_Game(Rules rules)
{
    m_designator = {0, 0, CGOL_EMPTY_STRING};
    m_grid = CellArray();
    m_live_cell_count = 0;
    m_is_warp = true;
    m_registered_games = GamesList();
    m_rule_spec = decode_rules(rules);
}


/// @brief CGOL_Game copy constructor
/// @param obj source CGOL_Game object
CGOL_Game::CGOL_Game(CGOL_Game const& obj)
{
    m_designator = obj.m_designator;
    m_grid = obj.m_grid;
    m_live_cell_count = obj.m_live_cell_count;
    m_is_warp = obj.m_is_warp;
    m_registered_games = obj.m_registered_games;
    m_rule_spec = obj.m_rule_spec;
}


/// @brief Designator used as return for failed load operations.
const Designator CGOL_Game::s_invalid_designator{Designator::INVALID};


/// @brief Create a new, empty game
/// @param shape {rows, cols} shape of the new game
/// @param name name of the new game; default=""
/// @param is_warp edge-warp status of the new game; default=true
/// @return game designator {rows, cols, name} for the new game
const Designator& CGOL_Game::new_game(array_shape_t shape, CGOL_STRING const& name, bool is_warp)
{
    m_grid = CellArray(shape);
    shape = m_grid.shape();  // get the shape as constructed
    m_designator = { shape.rows, shape.cols, name };
    m_is_warp = is_warp;
    m_live_cell_count = m_grid.live_count();
    return m_designator;
}


/// @brief Load game from pattern, overwriting any existing game
/// @param pattern cell array descriptor string
/// @param name name to assign to the game; default=""
/// @param is_warp edge-warp: true=warp at edge, false=do not warp at edge
/// @param shape optional shape {rows, cols}; default={0,0} -> use size from pattern
/// @param rules optional rules in B/S format (e.g. "B3/S23")
/// @return game designator {rows, cols, name} for the new game;
/// returns {"", 0, 0} upon failure
/// @note If a failure occurs, this function will not alter the current game.
const Designator& CGOL_Game::load_pattern(Pattern pattern, CGOL_STRING const& name, bool is_warp, array_shape_t shape, const Rules rules)
{
    try
    {   // this block will catch conversion errors and will not alter the
        // current game contents if an error occurs

        // exception will occur in this block if it occurs
        CellArray new_grid = CellArray(pattern);
        if (shape)
            new_grid.resize(shape, ANCHOR::X);
        RuleSpec new_rule_spec = decode_rules(rules);

        // now that it is validated, copy over our game
        shape = new_grid.shape();
        m_grid = new_grid;
        m_is_warp = is_warp;
        m_designator = { shape.rows, shape.cols, name };
        m_live_cell_count = m_grid.live_count();
        m_rule_spec = new_rule_spec;
    }
    catch (const std::exception& e)
    {   // invalid pattern or sizing error - return an invalid designator
        // to indicate failure
        return s_invalid_designator;
    }

    return m_designator;
}


/// @brief Load game from one of the presets (built-in or registered)
/// @param preset 0-based index to a preset
/// @return game designator {rows, cols, name} for the new game
const Designator& CGOL_Game::load_preset(int preset)
{
    GameSpec spec;
    size_t N_preset_games = AppConfig::CGOL_GAME_PRESETS.size();

    if (preset >= 0 && preset < N_preset_games)
        spec = AppConfig::CGOL_GAME_PRESETS[preset];
    else if (preset >= 0 && preset-N_preset_games < m_registered_games.size())
        spec = m_registered_games[preset-N_preset_games];
    else
        return s_invalid_designator;

    array_anchor_t anchor;
    switch (spec.anchor)
    {
        case 0: default:
            anchor = ANCHOR::X;
            break;

        case 1:
            anchor = ANCHOR::NW;
            break;

        case 2:
            anchor = ANCHOR::N;
            break;

        case 3:
            anchor = ANCHOR::NE;
            break;

        case 4:
            anchor = ANCHOR::W;
            break;

        case 5:
            anchor = ANCHOR::E;
            break;

        case 6:
            anchor = ANCHOR::SW;
            break;

        case 7:
            anchor = ANCHOR::S;
            break;

        case 8:
            anchor = ANCHOR::SE;
            break;
    }

    try
    {
        // exception will occur in this block if it occurs
        CellArray new_grid = CellArray(spec.pattern);
        new_grid.resize({spec.rows, spec.cols}, anchor);
        RuleSpec new_rule_spec = CGOL_Game::decode_rules(spec.rules);

        // now that it is validated, copy over our game
        m_grid = new_grid;
        m_is_warp = spec.is_warp;
        m_designator = { spec.rows, spec.cols, spec.name };
        m_live_cell_count = m_grid.live_count();
        m_rule_spec = new_rule_spec;
    }
    catch(const std::exception& e)
    {
        return s_invalid_designator;
    }

    return m_designator;
}


/// @brief Load a CGOL file into the CGOL_Game
/// @param filename
/// @return Designator for the loaded file
/// @note If the load was unsuccessful, the designator .name will be ""
const Designator& CGOL_Game::load_file(CGOL_STRING const& filename)
{
    CGOL_STRING file_snapshot = CGOL_EMPTY_STRING;

    try
    {
        std::ifstream file(filename.ToStdString());

        if (file)
        {
            std::stringstream buffer;
            buffer << file.rdbuf();
            file_snapshot = wxString::FromUTF8(buffer.str());
        }

        if (!file_snapshot.empty())
        {
            set_snapshot(file_snapshot);
            register_game();
        }
        else
        {
            return s_invalid_designator;
        }
    }
    catch(const std::exception& e)
    {
        return s_invalid_designator;
    }

    return m_designator;
}


/// @brief Add the current game to the list (overwrite if exists; add if not)
/// @note If name exists on preset-games list, mangles the new name before
// adding it to the registered games list.
void CGOL_Game::register_game()
{
    CGOL_STRING name = m_designator.name;

    // first, determine if it matches a preset game name
    const GamesList preset_games = AppConfig::CGOL_GAME_PRESETS;
    GamesList::const_iterator const_iter = std::find_if(
        preset_games.begin(),
        preset_games.end(),
        [&name](const GameSpec& item) { return item.name == name; }
    );

    if (const_iter != preset_games.end())
    {   // our game is in the list, mangle it
        name = name + " - user";
        m_designator.name = name;
    }

    // next, determine if it matches a registered game name
    GamesList reg_games = m_registered_games;
    GamesList::iterator iter = std::find_if(
        reg_games.begin(),
        reg_games.end(),
        [&name](const GameSpec& item) { return item.name == name; }
    );

    Rules rules = encode_rules(m_rule_spec);
    CGOL_STRING pattern = toGridString();
    GameSpec spec = { name, m_designator.rows, m_designator.cols, m_is_warp, rules, 0, pattern};

    if (iter != reg_games.end())
    {   // matched: overwrite it, but we need to find the full
        *iter = spec;
    }
    else
    {   // no match: add it
        m_registered_games.push_back(spec);
    }
}


/// @brief Sets the current game to the given snapshot
/// @param snapshot  snapshot string
/// @return  true if successful; false otherwise
bool CGOL_Game::set_snapshot(CGOL_STRING const& snapshot)
{
    try
    {
        std::wstringstream stream(snapshot.ToStdWstring());
        std::wstring line;
        CGOL_STRING read_line;
        CGOL_STRING name;
        long rows, cols;
        bool is_warp;
        Rules rules;

        // get the game name line
        if (!std::getline(stream, line)) return false;
        name = CGOL_STRING(line).Trim(false).Trim(true);

        // get the game specs line: rows, cols, is_warp, rules
        if (!std::getline(stream, line)) return false;
        read_line = CGOL_STRING(line).Trim(false).Trim(true);

        wxStringTokenizer tokenizer(read_line, wxT(","), wxTOKEN_STRTOK);
        wxString token;
        token = tokenizer.GetNextToken().Trim(false).Trim(true);
        token.ToLong(&rows);
        token = tokenizer.GetNextToken().Trim(false).Trim(true);
        token.ToLong(&cols);
        token = tokenizer.GetNextToken().Trim(false).Trim(true);
        is_warp = (token.Lower() == "true");
        token = tokenizer.GetNextToken().Trim(false).Trim(true);
        rules = token.Upper();

        // now, get the pattern
        std::wstringstream remains;
        remains << stream.rdbuf();
        read_line = remains.str();

        return bool(load_pattern(read_line, name, is_warp, {rows, cols}, rules));
    }
    catch(const std::exception& e)
    {
        return false;
    }

    return false;
}


/// @brief Get a snapshot of the game (essentially the text contents of a .cgol file)
/// @return string describing the current game state
CGOL_STRING CGOL_Game::get_snapshot(CGOL_STRING name) const
{
    return toString(name);
}


/// @brief Save the game to a .CGOL file
/// @param filename
/// @param name  optional name to save
/// @return true if successful; false otherwise
bool CGOL_Game::save_file(CGOL_STRING const& filename, CGOL_STRING const& name)
{
    try
    {
        bool result = false;
        CGOL_STRING game_snapshot;

        if (!name.empty())
        {
            game_snapshot = get_snapshot(name);
            m_designator.name = name;
        }
        else
        {
            CGOL_STRING stem;
            wxFileName::SplitPath(filename, nullptr, nullptr, &stem, nullptr);
            stem = stem.Trim(true).Trim(false);
            game_snapshot = get_snapshot(stem);
            m_designator.name = stem;
        }

        std::ofstream file(filename.ToStdString());

        if (file)
        {
            file << game_snapshot.ToUTF8();
            result = true;
            register_game();
        }

        return result;
    }
    catch(const std::exception& e)
    {
        return false;
    }

    return false;
}


/// @brief Get a list of the names of all games, preset and registered
/// @return vector containing the names of all games in indexed order
GamesNamesList CGOL_Game::get_games_names_list() const noexcept
{
    GamesNamesList my_list;

    // start with the built-in preset games
    for (auto game : AppConfig::CGOL_GAME_PRESETS)
    {
        my_list.push_back(game.name);
    }

    // now, add any games that have been added locally
    for (auto game : m_registered_games)
    {
        my_list.push_back(game.name);
    }

    return my_list;
}


/// @brief Get a list of all unique rules of games, preset and registered
/// @return vector containing the unique B/S rules for all games
RulesList CGOL_Game::get_rules_list() const noexcept
{
    RulesList my_list;

    // start with the built-in preset games
    for (auto game : AppConfig::CGOL_GAME_PRESETS)
    {
        bool found = std::find(my_list.begin(), my_list.end(), game.rules) != my_list.end();

        if (!found)
            my_list.push_back(game.rules);
    }

    // now, add any games that have been added locally
    for (auto game : m_registered_games)
    {
        bool found = std::find(my_list.begin(), my_list.end(), game.rules) != my_list.end();

        if (!found)
            my_list.push_back(game.rules);
    }

    return my_list;
}


/// @brief Clear the game grid
void CGOL_Game::clear()
{
    m_grid.clear();
    m_live_cell_count = 0;
}


/// @brief Change the size of the game grid
/// @param shape {rows, cols}; {0,0} -> do not change size
/// @param anchor anchor location for resize: default=NW
void CGOL_Game::resize(array_shape_t shape, array_anchor_t anchor)
{
    if (shape)
    {
        m_grid.resize(shape, anchor);
        shape = m_grid.shape();
        m_designator.rows = shape.rows;
        m_designator.cols = shape.cols;
    }
}


/// @brief Convert the CGOL game into a string representation
/// @return string representation of CGOL game
/// @note format of string representation:
///   1st row: name
///   2nd row: rows, cols, is_warp, rules
//    3rd+ rows: game grid representation
CGOL_STRING CGOL_Game::toString(CGOL_STRING name) const
{
    CGOL_STRING result;
    if (name.empty())
        result = m_designator.name + "\n";
    else
        result = name + "\n";
    CGOL_STRING str_is_warp = m_is_warp ? "True" : "False";
    CGOL_STRING str_rules = encode_rules(m_rule_spec);

    result += CGOL_FORMAT("%d, %d, %s, %s\n", m_designator.rows, m_designator.cols, str_is_warp, str_rules);
    result += m_grid.toString();

    return result;
}


/// @brief Convert the grid from the CGOL game into a string representation
/// @return game grid representation
CGOL_STRING CGOL_Game::toGridString() const
{
    return m_grid.toString();
}


/// @brief Game cell indexed write: game(row, col) = value
/// @param row 0-based row index
/// @param col 0-based column index
/// @return writeable reference to the indexed cell
const bool& CGOL_Game::operator() (int row, int col) const
{
    return m_grid(row, col);
}


/// @brief Game cell indexed read: value = game(row, col)
/// @param row 0-based row index
/// @param col 0-based column index
/// @return non-writeable reference to the indexed cell
bool& CGOL_Game::operator() (int row, int col)
{
    return m_grid(row, col);
}


/// @brief Apply cellular automaton rules to the game grid, warping at the edges
/// @param grid_now CellArray with current grid state
/// @param grid_next CellArray to receive the evolved grid state
/// @param rules RuleSpec with birth and survive sets
/// @return live cell count
void CGOL_Game::rules_warp_at_edge(const CellArray& grid_now, CellArray& grid_next, const RuleSpec& rules, size_t& live_cells)
{
    live_cells = 0;
    array_shape_t size = grid_next.shape();
    auto [nr, nc] = size;

    for (int i=0; i<nr; ++i)
    {   for (int j=0; j<nc; ++j)
        {   // get our current state of life
            bool life_now = grid_now(i, j);
            bool life_next = life_now;

            // count the 8 neighboring cells
            int live_neighbors = 0;
            for (int k=-1; k<=1; ++k)
            {
                if (grid_now(i+k, j-1))  live_neighbors += 1;
                if (grid_now(i+k, j+1))  live_neighbors += 1;
            }
            if (grid_now(i-1,j)) live_neighbors += 1;
            if (grid_now(i+1,j)) live_neighbors += 1;

            // apply the game rules
            if (life_now && !rules.survive.contains(live_neighbors))
                // living cell does not survive
                life_next = false;
            else if (!life_now && rules.birth.contains(live_neighbors))
                // dead cell is born
                life_next = true;

            // update the new cell
            if (life_next) live_cells += 1;
            grid_next(i, j) = life_next;
        }
    }
}


struct ArrayIndexHash {
    std::size_t operator()(const array_index_t& k) const noexcept
    {
        std::size_t h1 = std::hash<int>{}(k.r);
        std::size_t h2 = std::hash<int>{}(k.c);
        return h1 ^ (h2 + 0x9e3779b9 + (h1 << 6) + (h1 >> 2));
    }
};


/// @brief Algorithm to disintegrate structures that contact the border
/// @param grid CellArray with current grid state, also the target
/// @param live_cells contains the current count, also receives the count after
/// the disintegration.
void CGOL_Game::disintegrate_at_edge(CellArray& grid, size_t& live_cells)
{
    array_shape_t shape = grid.shape();
    auto [rows, cols] = shape;
    int r, c;
    array_index_t idx, idx_n;

    std::unordered_set<array_index_t, ArrayIndexHash> visited;
    std::unordered_set<array_index_t, ArrayIndexHash> to_kill;
    std::unordered_set<array_index_t, ArrayIndexHash> border_cells;
    std::queue<array_index_t> queue;

    // identify all live cells on the border
    for (r=0; r<rows; ++r)
    {
        idx = {r,0};
        if (grid[idx]) border_cells.insert(idx);
        idx.c = cols-1;
        if (grid[idx]) border_cells.insert(idx);
    }
    for (c=0; c<cols; ++c)
    {
        idx = {0,c};
        if (grid[idx]) border_cells.insert(idx);
        idx.r = rows-1;
        if (grid[idx]) border_cells.insert(idx);
    }

    // Breadth-First Search (BFS) algorithm to find the entire structure
    for (const auto& start_coord : border_cells)
    {
        if (visited.contains(start_coord))
            continue;
        visited.insert(start_coord);

        queue = {};
        to_kill.clear();
        queue.push(start_coord);

        while (!queue.empty())
        {
            idx = queue.front();
            queue.pop();
            to_kill.insert(idx);

            // check all 8 neighbor cells
            for (int dr=-1; dr<=1; ++dr)
            {   for (int dc=-1; dc<=1; ++dc)
                {
                    idx_n = { idx.r + dr, idx.c + dc };
                    if (shape.inside(idx_n.r, idx_n.c))
                    {   if (grid[idx_n] && !visited.contains(idx_n))
                        {
                            visited.insert(idx_n);
                            queue.push(idx_n);
                        }
                    }
                }
            }

            // disintegrate the entire structure
            for (const auto& kill : to_kill)
            {
                if (grid[kill])
                {
                    grid[kill] = false;
                    live_cells -= 1;
                }
            }
        }
    }
}


/// @brief Advance the cellular automaton to the next stage of evolution
/// @return live cell count after generation
size_t CGOL_Game::advance_generation()
{
    CellArray grid_now = m_grid;
    CellArray grid_next = CellArray(m_grid.shape());
    size_t live_cell_count = 0;
    rules_warp_at_edge(grid_now, grid_next, m_rule_spec, live_cell_count);
    if (!m_is_warp)
        disintegrate_at_edge(grid_next, live_cell_count);
    m_grid = grid_next;
    m_live_cell_count = live_cell_count;
    return m_live_cell_count;
}


/// @brief Add the given pattern at the specified position
/// @param pattern   Pattern to add (generally a small structure pattern)
/// @param pos       Position at which pattern will be added
void CGOL_Game::add_pattern_at(const Pattern& pattern, const array_index_t& pos)
{
    CellArray array(pattern);
    auto [r, c] = pos;
    auto [a_rows, a_cols] = array.shape();
    array_shape_t my_shape = m_grid.shape();

    for (int i=0; i<a_rows; ++i)
    {   for (int j=0; j<a_cols; ++j)
        {
            array_index_t idx = {r+i, c+j};

            if (!m_is_warp)
            {   // skip anything beyond our boundary
                if (idx.outside(my_shape))
                    continue;
            }

            bool old_cell = m_grid[idx];
            bool new_cell = array(i,j);

            if (new_cell != old_cell)
            {
                m_live_cell_count += (new_cell ? 1 : -1);
                m_grid[idx] = new_cell;
            }
        }
    }
}


/// @brief Decode rules into birth and survive sets
/// @param rules rules in B/S form (ex/ "B3/S23")
/// @return RuleSpec { birth, survive }
RuleSpec CGOL_Game::decode_rules(Rules const& rules)
{
    RuleSpec spec;
    spec.birth = {};
    spec.survive = {};

    enum decode_state
    {
        SEARCH_B,
        GET_BIRTH,
        SEARCH_S,
        GET_SURVIVE
    } state = SEARCH_B;

    for (auto ch : rules)
    {
        if (ch == ' ')
            continue;

        switch (state)
        {
            case SEARCH_B:
                // searching for 'B'
                if (ch=='B' || ch=='b')
                {
                    state = GET_BIRTH;
                    continue;
                }
                break;

            case GET_BIRTH:
                // searching for birth digits 1-8 for square grid
                if (ch>='0' && ch<='8')
                {
                    spec.birth.emplace(ch-'0');
                    continue;
                }
                else if (ch=='/')
                {
                    state = SEARCH_S;
                    continue;
                }
                break;

            case SEARCH_S:
                if (ch=='S' || ch=='s')
                {
                    state = GET_SURVIVE;
                    continue;
                }
                break;

            case GET_SURVIVE:
                // searching for survival digits 1-8 for square grid
                if (ch>='0' && ch<='8')
                {
                    spec.survive.emplace(ch-'0');
                    continue;
                }
                break;
        }

        // if we reach this point, break out of the loop
        break;
    }

    return spec;
}


/// @brief Encode RuleSpec into rules descriptor in B/S form
/// @param spec RuleSpec { birth, survive }
/// @return rules descriptor ex/ "B3/S23"
Rules CGOL_Game::encode_rules(RuleSpec const& spec)
{
    Rules rules;
    rules = "B";

    for ( int r : spec.birth )
        rules += char(r) + '0';

    rules += "/S";

    for ( int r : spec.survive )
        rules += char(r) + '0';

    return rules;
}


/*******************************************************************************
*  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
*  Unlicensed. Free for usage without warranty, expressed or implied
********************************************************************************/