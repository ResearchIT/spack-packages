# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-freesasa
#
# You can edit this file again by typing:
#
#     spack edit py-freesasa
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack_repo.builtin.build_systems.python import PythonPackage

from spack.package import *


class PyFreesasa(PythonPackage):
    """This module provides bindings for the FreeSASA C library."""

    homepage = "https://freesasa.github.io/python"
    pypi = "freesasa/freesasa-2.2.1.tar.gz"

    supplier =  "Simon Mitternacht"

    license("MIT", checked_by="snehring")

    version("2.2.1", sha256="5630e65d619cf6a062028d7c6297afe8c5b18c677c75f1c32a0938399f4f6850")

    depends_on("c", type="build")

    depends_on("py-setuptools", type="build")
    depends_on("py-cython@0.29.13:", type="build")
