#!/usr/bin/env python
from setuptools.extension import Extension

import sys
import os
import subprocess

from setuptools.command.build_py import build_py as _build_py
from setuptools import setup

def exec_generate_proto(source):
    protoc_command = ["python", "-m", "grpc_tools.protoc", "-I.", "--python_out=.", source]
    if subprocess.call(protoc_command) != 0:
        sys.exit(-1)
    sys.stdout.write("Generate {}_pb2.py ==> successfull\n".format(source.split('.')[0]))

    protoc_grpc_command = ["python", "-m", "grpc_tools.protoc", "-I.", "--python_out=.","--grpc_python_out=.", source]
    if subprocess.call(protoc_grpc_command) != 0:
        sys.exit(-1)
    sys.stdout.write("Generate {}_grcp_pb2.py ==> successfull\n".format(source.split('.')[0]))


ed25519_sha3_path = os.getcwd() + "cli/ed25519_sha3/"
sources = [ed25519_sha3_path+"ed25519_sha3module.c"]
sources.extend([ed25519_sha3_path+"lib/" + s for s in os.listdir(ed25519_sha3_path+"lib/") if s.endswith(".c")])
module_ed25519_sha3 = Extension("ed25519_sha3",include_dirs=[ed25519_sha3_path+"lib/"], sources=sources)

class GeneratePb(_build_py):
    def run(self):
        os.chdir("schema/")
        exec_generate_proto('block.proto')
        exec_generate_proto('commands.proto')
        exec_generate_proto('endpoint.proto')
        exec_generate_proto('primitive.proto')
        exec_generate_proto('queries.proto')
        exec_generate_proto('responses.proto')
        os.chdir("..")
        _build_py.run(self)

if __name__ == '__main__':
    setup(

          name='iroha-ya-cli',
          version='0.7',
          description='Cli for hyperledger/iroha',
          author='Sonoko Mizuki',
          license='Apache',
          author_email='mizuki.sonoko@gmail.com',
          packages = ['cli', 'schema'],
          ext_modules=[module_ed25519_sha3],
          include_package_data=True,
          install_requires=[
                'grpcio',
                'grpcio-tools',
                'protobuf',
                'PyYAML',

                'sha3',
                'ed25519'
          ],
          cmdclass={
            'build_py': GeneratePb,
          },
          entry_points={
          'console_scripts':
            ['iroha-ya-cli=cli.main:main']
          }
    )
