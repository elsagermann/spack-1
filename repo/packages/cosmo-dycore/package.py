##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class CosmoDycore(CMakePackage):
    """FIXME: Put a proper description of your package here."""
    
    homepage = "https://github.com/COSMO-ORG/cosmo/tree/master/dycore"
    git      = "git@github.com:COSMO-ORG/cosmo.git"
    maintainers = ['elsagermann']
    
    version('master', branch='master')

    variant('test', default=False, description="Compile Dycore unittests")
    variant('cosmo_target', default='gpu', description='Build target gpu or cpu', values=('gpu', 'cpu'), multi=False)
    variant('real_type', default='double', description='Build with double or single precision enabled', values=('double', 'float'), multi=False)
    variant('cuda_arch', default='none', description='Build with cuda_arch', values=('sm_70', 'sm_60', 'sm_37'), multi=False)
    
    depends_on('gridtools@1.1.3 cosmo_target=gpu', when='cosmo_target=gpu')
    depends_on('gridtools@1.1.3 cosmo_target=cpu', when='cosmo_target=cpu')
    depends_on('boost@1.67:')
    depends_on('serialbox@2.6.0%gcc', when='+test')
    depends_on('mpi')

    root_cmakelists_dir='dycore'
    
    def setup_environment(self, spack_env, run_env):
        spack_env.set('GRIDTOOLS_ROOT', self.spec['gridtools'].prefix)
        if self.spec.variants['test'].value:
          spack_env.set('SERIALBOX_ROOT', self.spec['serialbox'].prefix)

    def cmake_args(self):
      spec = self.spec

      args = []

      GridToolsDir = spec['gridtools'].prefix + '/lib/cmake'
      
      args.append('-DGridTools_DIR={0}'.format(GridToolsDir))  
      args.append('-DCMAKE_BUILD_TYPE=Release')
      args.append('-DCMAKE_INSTALL_PREFIX={0}'.format(self.prefix))
      args.append('-DCMAKE_FIND_PACKAGE_NO_PACKAGE_REGISTRY=ON')
      args.append('-DBoost_USE_STATIC_LIBS=ON')
      args.append('-DBOOST_ROOT={0}'.format(spec['boost'].prefix))
      args.append('-DDYCORE_ENABLE_PERFORMANCE_METERS=OFF')
      args.append('-DGT_ENABLE_BINDINGS_GENERATION=ON')
    
      if spec.variants['real_type'].value == 'float':
        args.append('-DPRECISION=float')
      else:
        args.append('-DPRECISION=double')
      
      if not spec.variants['test'].value:
          args.append('-DBUILD_TESTING=OFF')
      else:
          args.append('-DBUILD_TESTING=ON')
          SerialBoxRoot = spec['serialbox'].prefix + '/cmake'
          args.append('-DSerialbox_DIR={0}'.format(SerialBoxRoot))

      # target=gpu
      if self.spec.variants['cosmo_target'].value == 'gpu':
        args.append('-DENABLE_CUDA=ON')
        args.append('-DCUDA_ARCH={0}'.format(self.spec.variants['cuda_arch'].value))
        args.append('-DDYCORE_TARGET_ARCHITECTURE=CUDA')
      # target=cpu
      else:
        args.append('-DENABLE_CUDA=OFF')
        args.append('-DDYCORE_TARGET_ARCHITECTURE=x86')


      return args
