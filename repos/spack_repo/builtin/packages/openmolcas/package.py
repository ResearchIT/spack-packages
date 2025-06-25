# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack_repo.builtin.build_systems.cmake import CMakePackage

from spack.package import *


class Openmolcas(CMakePackage):
    """OpenMolcas is a quantum chemistry software package.
    The key feature of OpenMolcas is the multiconfigurational approach to
    the electronic structure."""

    homepage = "https://gitlab.com/Molcas/OpenMolcas"
    url = "https://gitlab.com/Molcas/OpenMolcas/-/archive/v25.06/OpenMolcas-v25.06.tar.gz"

    license("LGPL-2.1-or-later")

    version("25.06", sha256="df5262abd030d4fdfc66900140e608e53c71cf1d35acfdedcfaac147c02af94c")
    version("23.06", sha256="31727161c15ea588217c6511a3007792c74c35391849fa0296c2288d836cf951")
    version("21.02", sha256="d0b9731a011562ff4740c0e67e48d9af74bf2a266601a38b37640f72190519ca")
    version("19.11", sha256="8ebd1dcce98fc3f554f96e54e34f1e8ad566c601196ee68153763b6c0a04c7b9")

    variant("mpi", default=False, description="Build with mpi support.")
    variant("openmp", default=False, description="Build with openmp thread support.")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("hdf5")
    depends_on("lapack")
    depends_on("openblas+ilp64") #TODO expand this to supported blas implementations
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-pyparsing", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("mpi", when="+mpi")
    depends_on("globalarrays", when="+mpi")

    patch("CMakeLists.txt.patch", when="target=aarch64:")

    def setup_build_environment(self, env: EnvironmentModifications) -> None:
        env.set("MOLCAS", self.prefix)

    def setup_run_environment(self, env: EnvironmentModifications) -> None:
        env.set("MOLCAS", self.prefix)
        if self.spec.version >= Version("21.02"):
            env.append_path("PATH", self.prefix)

    def cmake_args(self):
        args = ["-DLINALG=OpenBLAS", "-DOPENBLASROOT=%s" % self.spec["openblas"].prefix, self.define_from_variant("OPENMP", "openmp")]
        if "+mpi" in self.spec:
            ga_path = self.spec["globalarrays"].prefix
            mpi_args = [
                "-DMPI=ON",
                "-DGA=ON",
                f"-DGA_INCLUDE_PATH={ga_path.include}",
                f"-DLIBGA={os.path.join(ga_path.lib, 'libga.so')}",
                f"-DLIBARMCI={os.path.join(ga_path.lib, 'libarmci.so')}",
            ]
            args.extend(mpi_args)
        return args
