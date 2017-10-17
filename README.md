
## YAC Yet Another Cli of Iroha

## How to use
ToDo
make config.yml in pwd
```config
peer:
    address:    localhost
    port:       50051
account:
    publicKey:  be98f280f22572686cbac3977f85be12176d72d45067ade75d81f6b5b626c138
    privateKey: 908ab4b8314044a3a7abc5f914dc96c822f0d3f469f132158ab2be6553fb4968f105fe252430f1a8f6bd635dc06ca3ec1055dea9128ae598e8540bf9666cfcff
    name:       mizuki
```
*It's sample, no problem


```
python ./cli.py CreateAsset --domain_id japan --precision 0 --asset_name yen
```


## Test
```
python -m unittest discover
```

### Prev
```
docker run -it -v  $(pwd)/iroha-mizuki-cli:/opt/iroha-mizuki-cli mizukisonoko/alpine-grpc-protobuf sh -c  "cd /opt/iroha-mizuki-cli; ls schema/*.proto | xargs -I{} sh -c 'protoc -I=./ --python_out=./ {}; protoc -I=./ --python_out=./ --grpc_out=./ --plugin=protoc-gen-grpc=`which grpc_python_plugin` {}'"
ls schema/*.proto | xargs sed -e '/^import "google.*/!s/import "/import "schema\//g' -i.bak
pip install -r requirements.txt 
```

## Env
- Python 3.5.0
- protobuf + grpc [mizukisonoko/alpine-grpc-protobuf](https://github.com/MizukiSonoko/alpine-grpc-protobuf)

## Recover protofile 
```
find schema -type f | sed 'p;s/.bak//' | xargs -n2 mv
```
