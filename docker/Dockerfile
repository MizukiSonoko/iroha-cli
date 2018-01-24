# Copyright 2018 Takeshi Yonezu. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#

FROM ubuntu:16.04

RUN apt update && apt upgrade -y
RUN apt install -y git gcc g++ cmake python3 python3-pip
RUN git clone https://github.com/MizukiSonoko/iroha-cli.git
RUN cd iroha-cli; \
    pip3 install -r requirements.txt; \
    python3 setup.py install; \
    python3 setup.py develop

CMD ["/bin/bash"]
