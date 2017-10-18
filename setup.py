#!/usr/bin/env python
import distutils
from distutils.core import setup
from distutils.extension import Extension

import sys

import subprocess

from distutils.command.build_py import build_py as _build_py


def exec_generate_proto(source):
    protoc_command = ["python", "-m", "grpc_tools.protoc", "-I.", "--python_out=.", source]
    if subprocess.call(protoc_command) != 0:
        sys.exit(-1)
    protoc_grpc_command = ["python", "-m", "grpc_tools.protoc", "-I.", "--python_out=.", source]
    if subprocess.call(protoc_grpc_command) != 0:
        sys.exit(-1)


class GeneratePb(_build_py):
    def run(self):
        sys.stdout.write("Generate *_pb2.py ...")
        base_path = "src/schema/"
        exec_generate_proto(base_path+'block.proto')
        exec_generate_proto(base_path+'commands.proto')
        exec_generate_proto(base_path+'endpoint.proto')
        exec_generate_proto(base_path+'primitive.proto')
        exec_generate_proto(base_path+'queries.proto')
        exec_generate_proto(base_path+'responses.proto')


if __name__ == '__main__':
    print('---')
    subprocess.call(["pwd"])
    setup(
          name='iroha-ya-cli',
          version='0.7',
          description='Cli for hyperledger/iroha',
          author='Sonoko Mizuki',
          author_email='mizuki.sonoko@gmail.com',
          packages=['src'],
          data_files=[
              ('share', ['README.md'])
          ],
          include_package_data=True,
          install_requires=[
                'grpcio',
                'grpcio-tools',
                'protobuf',

                'sha3',
                'ed25519'
          ],
          cmdclass={
            'build_py': GeneratePb,
          },
          entry_points={
          'console_scripts':
                'iroha-ya-cli = src.main:main'
          },
    )