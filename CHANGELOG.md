# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.15] - 2019-02-12
### Changed
- Changed hashing logic for circuit uniquification to use `hash(repr(cls))`
  instead of `object.__hash__(cls)`.

## [0.1.14] - 2019-02-07
### Fixed
- Fixed bug in verilog parsing when `target_modules = None`.

## [0.1.13] - 2019-02-07
### Added
- Added support for `opts["uniquify"]` to set the uniquification mode via
  `m.compile`. Suppored values are `"UNIQUIFY", "WARN", "ERROR"`.

### Fixed
- Fixed bug in uniquification error mode.

[Unreleased]: https://github.com/phanrahan/magma/compare/v0.1.15...HEAD
[0.1.15]: https://github.com/phanrahan/magma/compare/v0.1.14...v0.1.15
[0.1.14]: https://github.com/phanrahan/magma/compare/v0.1.13...v0.1.14
[0.1.13]: https://github.com/phanrahan/magma/compare/v0.1.12...v0.1.13
