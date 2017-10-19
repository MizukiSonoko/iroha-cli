
## YAC: Yet Another Cli of Iroha

[hyperledger/iroha](https://github.com/hyperledger/iroha) is open source, I want to contribute to it...  

## Simple install

```
$ git clone https://github.com/MizukiSonoko/iroha-cli.git
$ cd iroha-cli
$ pip install -r requirements.txt # Required compiling proto file
$ python setup.py build
$ python setup.py develop # I want to `python setup.py install`...
```

## How to use

#### 0) Make `keypair` in this.
```
$ iroha-ya-cli  keygen --account_name mizuki
```
Result
```
$ ls -lth | head  -n 3
total 56
-r--------   1 mizuki  staff    64B Oct 17 18:00 mizuki.pri
-r--------   1 mizuki  staff    64B Oct 17 18:00 mizuki.pub
```


#### 1) Make `config.yml` in pwd
This file contains target peer information and my account info.
```config
peer:
    address:    localhost
    port:       50051
account:
    publicKeyPath:  mizuki.pub
    privateKeyPath: mizuki.pri
    name:           mizuki
```


####  2) Check config is whether correct or not using `config`. 

```
$ iroha-ya-cli config

  Config  
 =========

 name      : mizuki
 publicKey : be98f280f22572686cbac3977f85be12176d72d45067ade75d81f6b5b626c138
 privateKey: 908ab**...**cfcff
 load from : config.yml
 targetPeer: localhost:50051

```

#### 3) Send tx like this

```
$ iroha-ya-cli CreateAsset --domain_id japan --precision 0 --asset_name yen
generated command: create_asset {
  asset_name: "yen"
  domain_id: "japan"
}

== Grpc happens error ==
- Server is active?: False 
- What's happen?   : Connect Failed 

Transaction is not arrived...
Could you ckeck this => localhost:50051

```
I sent. (This error is expected, no problem)

#### 4) You can know optin using `-h` or `--help` command.

In first, you can see all command use this.
```
iroha-ya-cli
```

In second, you can see detail of each command.
```
$ iroha-ya-cli CreateAsset -h
Create new asset in domain
-----------
Arguments
- precision : how much support .000, default 0
- domain_id : new account will be in this domain like japan
- asset_name: asset name like mizuki
```
 
## Sample

- CreateAsset 
```
iroha-ya-cli CreateAsset --domain_id japan --precision 0 --asset_name yen
```

- CreateAccount

```
iroha-ya-cli CreateAccount --account_name mizuki --domain_id japan
```

- CreateDomain

```
iroha-ya-cli CreateDomain --domain_name aizu
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
- Python 3.5.0
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