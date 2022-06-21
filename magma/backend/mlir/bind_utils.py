import abc
import pathlib

from magma.backend.mlir.common import wrap_with_not_implemented_error
from magma.backend.mlir.hw import hw
from magma.backend.mlir.magma_common import (
    visit_value_or_value_wrapper_by_direction as
    visit_magma_value_or_value_wrapper_by_direction
)
from magma.backend.mlir.mlir import MlirValue
from magma.backend.mlir.sv import sv
from magma.backend.mlir.utils import magma_type_to_mlir_type
from magma.circuit import CircuitKind
from magma.ref import get_ref_inst, get_ref_defn, Ref
from magma.t import Type
from magma.view import PortView


def _is_bound(ref: Ref) -> bool:
    return get_ref_inst(ref) is not None or get_ref_defn(ref) is not None


def _get_non_root_qualified_name(ctx: 'HardwareModule', ref: Ref) -> str:
    parts = ref.qualifiedname("^").split("^")
    defn = get_ref_defn(ref)
    if defn is not None:
        sep = "_" if ctx.opts.flatten_all_tuples else "."
        return sep.join(parts)
    inst = get_ref_inst(ref)
    assert inst is not None
    if ctx.opts.flatten_all_tuples:
        return f"{parts[0]}.{'_'.join(parts[1:])}"
    return ".".join(parts)


def _resolve_xmr(ctx: 'HardwareModule', xmr: PortView) -> MlirValue:
    assert isinstance(xmr, PortView)
    mlir_type = magma_type_to_mlir_type(type(xmr)._to_magma_())
    in_out = ctx.new_value(hw.InOutType(mlir_type))
    if ctx.opts.flatten_all_tuples:
        name = xmr.port.name.qualifiedname("_")
        path = list() if xmr.parent is None else list(xmr.parent.path())
        path = path + [name]
    else:
        path = list(xmr.path())
    sv.XMROp(is_rooted=False, path=path, results=[in_out])
    value = ctx.new_value(mlir_type)
    sv.ReadInOutOp(operands=[in_out], results=[value])
    return value


class _BindProcessorInterface(abc.ABC):
    def __init__(self, ctx: 'HardwareModule', defn: CircuitKind):
        self._ctx = ctx
        self._defn = defn

    @abc.abstractmethod
    def preprocess(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def process(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def postprocess(self):
        raise NotImplementedError()


class _NativeBindProcessor(_BindProcessorInterface):
    def preprocess(self):
        for bind_module in self._defn.bind_modules:
            # TODO(rsetaluri): Here we should check if @bind_module has already
            # been compiled, in the case that the bound module is either used
            # multiple times or is also a "normal" module that was compiled
            # elsewhere. Currently, the `set_hardware_module` call will raise an
            # error if @bind_module has been compiled already.
            hardware_module = self._ctx.parent.new_hardware_module(bind_module)
            hardware_module.compile()
            assert hardware_module.hw_module is not None
            self._ctx.parent.set_hardware_module(
                bind_module, hardware_module.hw_module)

    @wrap_with_not_implemented_error
    def _resolve_arg(self, arg) -> MlirValue:
        if isinstance(arg, Type):
            # NOTE(rsetaluri): We check that @arg is either a port or named
            # (temporary) value. If it is a named temporary, then we use the
            # name directly in an XMR op (we additionally assume that it is at
            # the same level of hierarchy).
            T = type(arg).undirected_t
            ref = arg.name
            if _is_bound(ref):
                if ref.root() is not ref:
                    name = _get_non_root_qualified_name(self._ctx, ref)
                    arg = T(name=name)
                    arg = PortView[T](arg, None)
                    return _resolve_xmr(self._ctx, arg)
                return self._ctx.get_mapped_value(arg)
            if ref.anon():
                raise TypeError(f"{arg}: anon bind arguments not supported")
            port_view = PortView[T](arg, None)
            return _resolve_xmr(self._ctx, port_view)
        if isinstance(arg, PortView):
            return _resolve_xmr(self._ctx, arg)

    def process(self):
        self._syms = []
        for bind_module, (args, _) in self._defn.bind_modules.items():
            operands = []
            for port in self._defn.interface.ports.values():
                visit_magma_value_or_value_wrapper_by_direction(
                    port,
                    lambda p: operands.append(self._ctx.get_mapped_value(p)),
                    lambda p: operands.append(self._ctx.get_mapped_value(p)),
                    flatten_all_tuples=self._ctx.opts.flatten_all_tuples,
                )
            operands += list(map(self._resolve_arg, args))
            inst_name = f"{bind_module.name}_inst"
            sym = self._ctx.parent.get_or_make_mapped_symbol(
                (self._defn, bind_module),
                name=f"{self._defn.name}.{inst_name}",
                force=True)
            module = self._ctx.parent.get_hardware_module(bind_module)
            inst = hw.InstanceOp(
                name=inst_name,
                module=module,
                operands=operands,
                results=[],
                sym=sym)
            inst.attr_dict["doNotPrint"] = 1
            self._syms.append(sym)

    def postprocess(self):
        defn_sym = self._ctx.parent.get_mapped_symbol(self._defn)
        for sym in self._syms:
            instance = hw.InnerRefAttr(defn_sym, sym)
            sv.BindOp(instance=instance)
        if self._syms:
            self._ctx.parent.add_bind_file(f"{self._ctx.opts.basename}.sv")


class _CoreIRBindProcessor(_BindProcessorInterface):
    def preprocess(self):
        return

    def process(self):
        for name, content in self._defn.compiled_bind_modules.items():
            path = pathlib.Path(self._ctx.opts.basename).parent
            filename = path / f"{name}.sv"
            with open(filename, "w") as f:
                f.write(content)
            self._ctx.parent.add_bind_file(filename.name)

    def postprocess(self):
        return


def make_bind_processor(ctx: 'HardwareModule', defn: CircuitKind):
    if ctx.opts.use_native_bind_processor:
        return _NativeBindProcessor(ctx, defn)
    return _CoreIRBindProcessor(ctx, defn)
