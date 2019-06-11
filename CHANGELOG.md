# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.9]
### Added
- Added `concat` instance method for array types, example:
  `a[0:-1].concat(m.bits(0, 1))`
- Added `coreir_libs` option to coreir compile command (https://github.com/phanrahan/magma/pull/406)

## [1.0.8]
### Added
- https://github.com/phanrahan/magma/pull/399 adds support for `+` in the
  verilog parser
- https://github.com/phanrahan/magma/pull/397 adds a new implementation of
  mergewires for better performance (use debug mode for the old implementation)

### Fixed
- https://github.com/phanrahan/magma/pull/401 fixes performance issue in
  verilog parsing

## [1.0.4] - 2019-04-25
### Fixed
- Fixed bug in coreir backend's handling of inout ports

## [1.0.2] - 2019-04-24
### Fixed
- Fixed bug in `BFloatKind` to remove second `__getitem__` definition

## [1.0.0] - 2019-03-20
### Changed
https://github.com/phanrahan/magma/pull/369
New `Array` and `Bits` type constructor syntax. Rather than parenthesis for type
constructors, we use square brackets: `Bits[8]` or `Array[3, Bit]`. This is to
have parity with the new `hwtypes` metaclass and typing system.

Also updates to the `m.sequential` syntax and code generation.

## [0.1.20] - 2019-03-19
### Fixed
Update to use hwtypes instead of bit_vector.

## [0.1.19] - 2019-02-25
### Fixed
- Fixes issue with renamed input ports in `m.circuit.combinational`
  (https://github.com/phanrahan/magma/pull/361)

## [0.1.18] - 2019-02-22
### Fixed
- Fixes installation issue where `magma.ssa` was not installed as a package


## [0.1.17] - 2019-02-21
### Fixed
- Fixes installation issue where `magma.syntax` was not installed as a package

## [0.1.16] - 2019-02-21
### Addded
- https://github.com/phanrahan/magma/pull/354
  Added experimental version of `m.circuit.sequential` syntax.
### Changed
- https://github.com/phanrahan/magma/pull/354
  Changes `m.circuit.combinational` to use SSA
### Fixed
- https://github.com/phanrahan/magma/pull/355
  Fixes regression in sorting logic for instance graph pass introduced due to
  new hashing logic. Changed uniquification to hash on the rep of the
  definition explicitly, rather than overriding the `__hash__` method of
  circuit
- https://github.com/phanrahan/magma/pull/358
  Fixes invocation of pass to use new option syntax for coreir

## [0.1.15] - 2019-02-12
### Changed
- Changed hashing logic for circuit uniquification to use `hash(repr(cls))`
  instead of `object.__hash__(cls)`.

### Fixed
- Run uniquification before compiling circuit for the coreir simulator.

## [0.1.14] - 2019-02-07
### Fixed
- Fixed bug in verilog parsing when `target_modules = None`.

## [0.1.13] - 2019-02-07
### Added
- Added support for `opts["uniquify"]` to set the uniquification mode via
  `m.compile`. Suppored values are `"UNIQUIFY", "WARN", "ERROR"`.

### Fixed
- Fixed bug in uniquification error mode.

[Unreleased]: https://github.com/phanrahan/magma/compare/v0.1.18...HEAD
[0.1.19]: https://github.com/phanrahan/magma/compare/v0.1.18...v0.1.19
[0.1.18]: https://github.com/phanrahan/magma/compare/v0.1.17...v0.1.18
[0.1.17]: https://github.com/phanrahan/magma/compare/v0.1.16...v0.1.17
[0.1.16]: https://github.com/phanrahan/magma/compare/v0.1.15...v0.1.16
[0.1.15]: https://github.com/phanrahan/magma/compare/v0.1.14...v0.1.15
[0.1.14]: https://github.com/phanrahan/magma/compare/v0.1.13...v0.1.14
[0.1.13]: https://github.com/phanrahan/magma/compare/v0.1.12...v0.1.13
