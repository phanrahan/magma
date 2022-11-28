// From https://github.com/Kuree/kratos/blob/master/python/kratos_python.cc
#include <filesystem>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

std::optional<std::pair<std::string, uint32_t>> get_fn_ln(uint32_t num_frame_back) {
    // get caller frame info
    PyFrameObject *frame = PyThreadState_Get()->frame;
    uint32_t i = 0;
    while (frame->f_back && (++i) < num_frame_back) {
        frame = frame->f_back;
    }
    if (frame) {
        uint32_t line_num = PyFrame_GetLineNumber(frame);
        struct py::detail::string_caster<std::string> repr;
        py::handle handle(frame->f_code->co_filename);
        repr.load(handle, true);
        if (repr) {
            // resolve full path
            std::string filename =
                std::filesystem::absolute(std::string(repr));
            return std::make_pair(filename, line_num);
        }
    }
    return std::nullopt;
}

PYBIND11_MODULE(magma_debug, m) {
    m.doc() = R"pbdoc(
        .. currentmodule:: magma_debug
    )pbdoc";

    m.def("get_fn_ln", []() {
       return get_fn_ln(2);
    })
    .def("get_fn_ln", [](uint32_t num_frame) {
        return get_fn_ln((num_frame));
    });
}
