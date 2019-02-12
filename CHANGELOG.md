# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.15] - 2019-02-07
### Changed
- Changed hashing logic for circuit uniquification to use `hash(repr(cls))`
  instead of `object.__hash__(cls)`.

## [1.0.14] - 2019-02-07
### Fixed
- Fixed bug in verilog parsing when `target_modules = None`.

## [1.0.13] - 2019-02-07
### Added
- Added support for `opts["uniquify"]` to set the uniquification mode via
  `m.compile`. Suppored values are `"UNIQUIFY", "WARN", "ERROR"`.

### Fixed
- Fixed bug in uniquification error mode.

[Unreleased]: https://github.com/phanrahan/magma/compare/v1.0.14...HEAD
[1.0.14]: https://github.com/phanrahan/magma/compare/v1.0.13...v1.0.14
[1.0.13]: https://github.com/phanrahan/magma/compare/v1.0.12...v1.0.13
