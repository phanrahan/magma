cmake_minimum_required(VERSION 3.10)
project(magma_debug)

set(CMAKE_CXX_STANDARD 17)

add_subdirectory(pybind11)

set(PYBIND11_CPP_STANDARD -std=c++17)

set(CMAKE_EXE_LINKER_FLAGS " -static")

CHECK_CXX_COMPILER_FLAG(-static-libgcc COMPILER_STATIC)
if (${COMPILER_STATIC})
    # we also need to hide all symbols, other we will run into cxx string ABI issue
    # https://stackoverflow.com/a/57077456
    set(STATIC_FLAG "-static-libgcc -static-libstdc++")
    if(UNIX AND NOT APPLE)
        # only for Linux
        set(STATIC_FLAG ${STATIC_FLAG} -Wl,--exclude-libs,ALL)
    endif()
else()
    set(STATIC_FLAG "")
endif()

pybind11_add_module(magma_debug debug.cc)
target_link_libraries(magma_debug PUBLIC ${STATIC_FLAG})

set_target_properties(magma_debug PROPERTIES PREFIX "${PYTHON_MODULE_PREFIX}"
        SUFFIX "${PYTHON_MODULE_EXTENSION}" COMPILE_FLAGS "-Wno-register")

if ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang")
    set_target_properties(magma_debug PROPERTIES COMPILE_FLAGS -fsized-deallocation)
endif()
