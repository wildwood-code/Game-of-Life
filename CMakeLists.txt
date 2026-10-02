#*******************************************************************************
#  Unlicensed. Free for usage without warranty, expressed or implied
#
#  Implementation of Conway's Game of Life
#
#  Filename   : CMakeLists.txt
#  Description:
#    This C++ program implements a simple zero-player game known as
#    Conway's Game of Life (CGoL). CGoL was devised by John Horton Conway in
#    1970.  https://en.wikipedia.org/wiki/Conway's_Game_of_Life
#
#    This file specifies the CMake sources and target, and CPack info.
#
#  Change log:
#    2026-09-26  KSM  Created
#
#  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
#*******************************************************************************

# ==========================================
# CMAKE SECTION
# ==========================================

cmake_minimum_required(VERSION 3.15)

# Set the internal project identifier
project(GameOfLife VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Generate cgol_version.h from the template
configure_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/src/cgol_version.h.in"
    "${CMAKE_CURRENT_BINARY_DIR}/cgol_version.h"
)

# Target environment explicit routing
set(wxWidgets_ROOT_DIR "C:/Tools/wxWidgets")
set(wxWidgets_USE_STATIC ON)

# Point CMake directly to the compiled MSVC static library binaries folder.
# (If your build is 64-bit, this folder is usually named "vc_x64_lib" instead of "vc_lib")
set(wxWidgets_LIB_DIR "C:/Tools/wxWidgets/lib/vc_x64_lib")
set(wxWidgets_CONFIGURATION msvc)

# Find your wxWidgets installation
find_package(wxWidgets REQUIRED COMPONENTS net core base)
include(${wxWidgets_USE_FILE})

# Gather all source files in the root folder
set(SOURCES
    "src/main.cpp"
    "src/app_config.cpp"
    "src/cgol_frame.cpp"
    "src/panel_grid.cpp"
    "src/cgol_images.cpp"
    "src/cgol_game.cpp"
    "src/cell_array.cpp"
    "src/about.cpp"
    "src/grid_menu.cpp"
    "src/rules_dialog.cpp"
    "src/size_dialog.cpp"
    "src/generated/generated_ui.cpp"
    "src/cgol_app.rc"
)

# This routes the executable to ../dist/debug or ../dist/release based on the active variant
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG "${CMAKE_CURRENT_SOURCE_DIR}/dist/debug")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE "${CMAKE_CURRENT_SOURCE_DIR}/dist/release")

# Define the final executable name
add_executable(GameOfLife WIN32 ${SOURCES})

# Add MSVC-specific compiler options for your executable target
if(MSVC)
    target_compile_options(GameOfLife PRIVATE /utf-8)
endif()

# Include directory helper for the subdirectory files
target_include_directories(GameOfLife PRIVATE "${CMAKE_CURRENT_SOURCE_DIR}/app/generated")
target_include_directories(GameOfLife PRIVATE "${CMAKE_CURRENT_BINARY_DIR}")

# Link the compiled wxWidgets libraries to your executable
target_link_libraries(GameOfLife PRIVATE ${wxWidgets_LIBRARIES})

# install the executable
install(TARGETS GameOfLife DESTINATION .)


# ==========================================
# CPACK SECTION
# ==========================================

# Includes standard MSVC/system runtime library dlls (like vcruntime140.dll)
# comment out to disable
include(InstallRequiredSystemLibraries)

# Configure packaging details
set(CPACK_PACKAGE_NAME "GameOfLife")
set(CPACK_PACKAGE_VENDOR "WWES")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Conway's Game of Life")
set(CPACK_PACKAGE_VERSION "${PROJECT_VERSION}")

# Choose installer formats (e.g., ZIP archive and NSIS setup wizard for Windows)
set(CPACK_GENERATOR "ZIP")

# Set the destination
set(CPACK_PACKAGE_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/dist")

# Finally, generate the packaging targets
include(CPack)


#*******************************************************************************
#  Copyright © 2026 Kerry S Martin, wssm243@gmail.com
#  Unlicensed. Free for usage without warranty, expressed or implied
#*******************************************************************************