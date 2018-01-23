#!/usr/bin/env python 
import shutil
from setuptools.extension import Extension

import sys
import os
import subprocess

from setuptools.command.build_py import build_py as _build_py
from setuptools import setup, find_packages

def exec_generate_proto(source,python):
    protoc_command = [ python, "-m", "grpc_tools.protoc", "-I.", "--python_out=.", source]
    if subprocess.call(protoc_command) != 0:
        sys.exit(-1)
    sys.stdout.write("Generate {}_pb2.py ==> successfull\n".format(source.split('.')[0]))

    protoc_grpc_command = [ python, "-m", "grpc_tools.protoc", "-I.", "--python_out=.","--grpc_python_out=.", source]
    if subprocess.call(protoc_grpc_command) != 0:
        sys.exit(-1)
    sys.stdout.write("Generate {}_grcp_pb2.py ==> successfull\n".format(source.split('.')[0]))

def check_python_grpc(python):
    protoc_command = [python, "-m", "grpc_tools.protoc", "--version"]
    return subprocess.call(protoc_command) == 0

class GeneratePb(_build_py):
    def run(self):
        python = shutil.which("python3")
        if not python or not check_python_grpc(python):
            python = shutil.which("python")

        os.chdir("iroha_cli_schema/")
        exec_generate_proto('block.proto',python)
        exec_generate_proto('commands.proto',python)
        exec_generate_proto('endpoint.proto',python)
        exec_generate_proto('primitive.proto',python)
        exec_generate_proto('queries.proto',python)
        exec_generate_proto('responses.proto',python)
        os.chdir("..")
        _build_py.run(self)

if __name__ == '__main__':
    setup(
          name='iroha-ya-cli',
          version='1.2.10',
          description='Cli for hyperledger/iroha',
          author='Sonoko Mizuki',
          license='Apache',
          author_email='mizuki.sonoko@gmail.com',
          packages = find_packages(),
          include_package_data=True,
          install_requires=[
                'grpcio',
                'grpcio-tools',
                'protobuf',
                'PyYAML',

                'ed25519-python'
          ],
          cmdclass={
            'build_py': GeneratePb,
          },
          classifiers=[
             'Programming Language :: Python :: 3.5',

             'Development Status :: 4 - Beta',

             'License :: OSI Approved :: Apache Software License',
             'Topic :: Utilities'
          ],
          entry_points={
          'console_scripts':
            ['irohac=iroha_cli.main:main']
          }
    )
