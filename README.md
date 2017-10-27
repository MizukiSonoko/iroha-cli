
## YAC: Yet Another Cli of Iroha
[![CircleCI](https://circleci.com/gh/MizukiSonoko/iroha-cli.svg?style=shield)](https://circleci.com/gh/MizukiSonoko/iroha-cli)

[hyperledger/iroha](https://github.com/hyperledger/iroha) is open source, I want to contribute to it...  

## Suppert version  

- python2.7 => ToDo
- python3.4 => ToDo
- python3.5 => ⚪️ 
- python3.6 => ToDo


## Simple install

```
$ pip install iroha-ya-cli
```

## How to use

#### 0) Make `keypair` and `config.yml` in this.
```
$ iroha-ya-cli keygen  --account_name mizuki --make_conf yes
```

Result
```
$ ls -lth | head  -n 4
total 76K
-rw-r--r--   1 mizuki staff  122 Oct 27 07:38 config.yml
-rw-r--r--   1 mizuki staff   88 Oct 27 07:38 mizuki.pri
-rw-r--r--   1 mizuki staff   44 Oct 27 07:38 mizuki.pub
```
**Please change permission for protect key!!**

#### 1) Change information in generated `config.yml` 
This file contains target peer information and my account info.
```config
account:
  name: mizuki
  privateKeyPath: mizuki.pri
  publicKeyPath: mizuki.pub
peer:
  address: localhost
  port: 50051
```
Peer is target where cli send tx to. I guess Iroha uses grpc, so port is 50051.

####  2) Check config is whether correct or not using `config` command. 

```
$ iroha-ya-cli config --config config.yml

  Config
 =========

 name      : mizuki
 publicKey : d5MxIVcHE2eq883JFYxkQVKZV794hWqR2VnXj/iSU1A=
 privateKey: GOcAK**...**Gvg==
 targetPeer: localhost:50051

```

#### 3) Send tx like this

```
$ iroha-ya-cli tx  CreateAsset --domain_id japan --precision 0 --asset_name yen --config config.yml
== Grpc happens error ==
- Server is active?: False
- What's happen?   : Connect Failed

Transaction is not arrived...
Could you ckeck this => localhost:50051

```
I sent. (This error is expected, no problem 😅 😅 )

#### 4) You can know optin using `-h` or `--help` command.

In first, you can see all command use this.
```
iroha-ya-cli
```

In second, you can see detail of each command.
```
$ iroha-ya-cli tx CreateAsset -h
usage: iroha-ya-cli tx CreateAsset [-h] --asset_name ASSET_NAME --domain_id
                                   DOMAIN_ID [--precision PRECISION]
                                   [--config CONFIG]

optional arguments:
  -h, --help            show this help message and exit
  --asset_name ASSET_NAME
                        asset name like mizuki
  --domain_id DOMAIN_ID
                        new account will be in this domain like japan
  --precision PRECISION
                        how much support .000, default 0
  --config CONFIG       config.yml's path
  
```
 
## Sample

- CreateAsset 
```
iroha-ya-cli tx CreateAsset --domain_id japan --precision 0 --asset_name yen --config config.yml
```

- CreateAccount

```
iroha-ya-cli tx CreateAccount --account_name mizuki --domain_id japan --config config.yml
```

- CreateDomain

```
iroha-ya-cli tx CreateDomain --domain_name aizu --config config.yml
```

....


## Test
```
python -m unittest discover
```

## Develop
```
# Compile protofile 
git clone https://github.com/MizukiSonoko/iroha-cli.git
cd iroha-cli
docker run -it -v  $(pwd):/opt/iroha-mizuki-cli mizukisonoko/alpine-grpc-protobuf sh -c  "cd /opt/iroha-mizuki-cli/schema; ls *.proto | xargs -I{} sh -c 'protoc -I=./ --python_out=../ {}; protoc -I=./ --python_out=../ --grpc_out=../ --plugin=protoc-gen-grpc=`which grpc_python_plugin` {}'"
pip install -r requirements.txt 
```




## Env
- protobuf + grpc [mizukisonoko/alpine-grpc-protobuf](https://github.com/MizukiSonoko/alpine-grpc-protobuf)



## Tips

It happens this
```
Running PyYAML-3.12/setup.py -q bdist_egg --dist-dir /tmp/easy_install-wwituzoz/PyYAML-3.12/egg-dist-tmp-kgc91i9t
build/temp.linux-x86_64-3.5/check_libyaml.c:2:18: fatal error: yaml.h: No such file or directory
compilation terminated.

libyaml is not found or a compiler error: forcing --without-libyaml
```
=> `apt install -y libyaml-dev`
