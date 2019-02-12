# Release Process
Magma is released on [pypi](https://pypi.org/) under the package
[magma-lang](https://pypi.org/project/magma-lang/).  @leonardt is the current
maintainer of the package, but releases are typically managed through Travis.

To release a new version:
1. Update [CHANGELOG.md](../CHANGELOG.md) with the changes that will be
   included in the release. See
   [keepachangelog.com](https://keepachangelog.com/en/1.0.0/) for some tips on
   how to keep a good changelog.
2. Update [setup.py](../setup.py) with the next version number.  Follow the
   guidelines for [semantic versioning](https://semver.org/)
3. Commit your changes and tag with the release (e.g. `git tag v1.0.15`)
4. Push your changes including the new tag `git push && git push --tags`
5. Monitor the Travis build for the tagged commit. If it succeeds, the log
   should indicate that the latest release was uploaded to PyPI.
