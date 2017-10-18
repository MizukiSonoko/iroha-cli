#!/usr/bin/env python
import distutils
from distutils.core import setup
from distutils.extension import Extension

import sys

import subprocess


def exec_generate_proto( protoc, source):
    protoc_command = [protoc, "-I.", "--python_out=.", source]
    if subprocess.call(protoc_command) != 0:
        sys.exit(-1)
    protoc_grpc_command = [protoc, "-I.", "--python_out=.", "--grpc_python_out =.", source]
    if subprocess.call(protoc_grpc_command) != 0:
        sys.exit(-1)


class GeneratePb(distutils.command.install_data.install_data):
    def run(self):
        protoc = "python3 -m grpc_tools.protoc"
        exec_generate_proto(protoc,'schema/block.proto')
        exec_generate_proto(protoc,'schema/commands.proto')
        exec_generate_proto(protoc,'schema/endpoint.proto')
        exec_generate_proto(protoc,'schema/primitive.proto')
        exec_generate_proto(protoc,'schema/queries.proto')
        exec_generate_proto(protoc,'schema/responses.proto')




if __name__ == '__main__':

    setup(
          name='iroha-ya-cli',
          version='0.7',
          description='Cli for hyperledger/iroha',
          author='Sonoko Mizuki',
          author_email='mizuki.sonoko@gmail.com',
          packages=['src'],
          data_files=[
              ('schema', ["schema/*"])
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
            "generate_pb": GeneratePb
          },
          entry_points={
          'console_scripts':
                'iroha-ya-cli = src.main:main'
          },
    )