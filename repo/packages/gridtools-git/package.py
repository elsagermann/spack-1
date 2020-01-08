# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
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
#     spack install gridtools-git
#
# You can edit this file again by typing:
#
#     spack edit gridtools-git
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class GridtoolsGit(CMakePackage):
    """The GridTools framework is a set of libraries and utilities to develop performance portable applications in the area of weather and climate."""

    git = "git@github.com:GridTools/gridtools.git"

    maintainers = ['elsagermann']
    
    version('master', branch='master')
    version('1.1.0', commit='12ee09103bcd46edb978259b59e90d611f32ed01')
    version('1.0.3', commit='8468d2000ccec95d3a1c481664e6b41a0b038413')
    version('1.0.2', commit='2d42ea7d7639de1b52a2106e049a21cfea7192ea')
    version('1.0.1', commit='11053321adac080abee0c6d8399ed6a63479bb48')
    version('1.0.0', commit='5dfeace6f20eefa6633102533d5a0e1564361ecf')

    depends_on('ncurses')
    depends_on('cmake')
    depends_on('boost')

    def cmake_args(self):
      spec = self.spec
      args = []

      args.append('-DGT_INSTALL_EXAMPLES=OFF')
      args.append('-DBUILD_TESTING=OFF')
      args.append('-DBUILD_SHARED_LIBS=OFF')
      #args.append('-DGT_USE_MPI=ON')
      args.append('-DBoost_NO_BOOST_CMAKE=ON')
     #args.append('-DCMAKE_BUILD_TYPE:STRING="Release"')
      args.append('-DGT_ENABLE_BINDINGS_GENERATION=ON')
      args.append('-DCMAKE_EXPORT_NO_PACKAGE_REGISTRY=ON')
     # -DBOOST_ROOT="$DEFAULT_BOOST_ROOT"
      return args

