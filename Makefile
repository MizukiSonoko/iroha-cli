# Copyright 2018 Takeshi Yonezu All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

.PHONY: all test

UKERNEL := $(shell uname -s)
UMACHINE := $(shell uname -m)

ifeq ($(UKERNEL),Linux)
  ifeq ($(UMACHINE),x86_64)
    PROJECT := hyperledger
    DOCKER := Dockerfile
  endif
  ifeq ($(UMACHINE),armv7l)
    PROJECT := arm32v7
    DOCKER := Dockerfile.arm32v7
  endif
endif

ifeq ($(UKERNEL),Darwin)
  PROJECT := hyperledger
  DOCKER := Dockerfile
endif

ifeq ($(DOCKER), )
$(error This platform "$(UKERNEL)/$(UMACHINE)" in not supported.)
endif

all:
	cd docker; docker build --rm -t $(PROJECT)/irohac -f $(DOCKER) .

test:
	cd example; bash test.sh
