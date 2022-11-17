cmake_minimum_required(VERSION 3.10)
project(magma_debug)

set(CMAKE_CXX_STANDARD 17)

add_subdirectory(pybind11)

set(PYBIND11_CPP_STANDARD -std=c++17)

set(CMAKE_EXE_LINKER_FLAGS " -static")

pybind11_add_module(_magma_debug debug.cc)
target_link_libraries(_magma_debug PUBLIC ${STATIC_FLAG})

set_target_properties(_magma_debug PROPERTIES PREFIX "${PYTHON_MODULE_PREFIX}"
        SUFFIX "${PYTHON_MODULE_EXTENSION}" COMPILE_FLAGS "-Wno-register")

if ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang")
    set_target_properties(_magma_debug PROPERTIES COMPILE_FLAGS -fsized-deallocation)
endif()
