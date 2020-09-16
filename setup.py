#!/usr/local/bin/python3

# -*- coding: UTF-8 -*-
# python3 setup.py build_ext --inplace
# import distutils.core
# import Cython.Build

# distutils.core.setup(
#     always_allow_keywords=True,
#     c_string_encoding='utf-8',
#     language_level=3,
#     ext_modules=Cython.Build.cythonize(
#         "baidu_com.py"
#     )
# )

import os
import re

from distutils.core import Extension, setup
from Cython.Build import cythonize
from Cython.Compiler import Options
 
 
# __file__ 含有魔术变量的应当排除，Cython虽有个编译参数，但只能设置静态。
exclude_so = ['__init__.py', "mixins.py"]
sources = ['.', 'core', 'libs']
 
 
extensions = []
for source in sources:
    for dirpath, foldernames, filenames in os.walk(source):
        for filename in filter(lambda x: re.match(r'.*[.]py$', x), filenames):
            file_path = os.path.join(dirpath, filename)
            if filename not in exclude_so:
                print('>>>>>>>>>>', filename[:-3], file_path)
                extensions.append(Extension(filename[:-3], [file_path], extra_compile_args = ["-Os", "-g0"]))
                        # Extension(file_path[:-3].replace('/', '.'), [file_path], extra_compile_args = ["-Os", "-g0"],
                        #           extra_link_args = ["-Wl,--strip-all"]))
 
 
print('>>>>>>>>>>>>>', extensions)
Options.docstrings = False
compiler_directives = {'optimize.unpack_method_calls': False}
setup(  
        # cythonize的exclude全路径匹配，不灵活，不如在上一步排除。
        ext_modules = cythonize(extensions, exclude = None, nthreads = 20, quiet = True, build_dir = './build',
                                language_level =3, compiler_directives = compiler_directives))