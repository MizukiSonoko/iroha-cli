# Copyright 2018 Takeshi Yonezu. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#

FROM ubuntu:16.04

RUN apt update && apt-get -y upgrade

RUN apt -y install cmake gcc g++ git \
    python3 python3-pip \
 && apt -y clean

RUN git clone https://github.com/MizukiSonoko/iroha-cli.git \
 && cd iroha-cli; \
    pip3 install -r requirements.txt \
 && python3 setup.py install \
 && python3 setup.py develop

CMD ["/bin/bash"]
