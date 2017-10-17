
## YAC Yet Another Cli of Iroha

## How to use
ToDo
```
python ./cli.py 
```


## Test
```
python -m unittest discover
```

### Prev
```
ls schema/*.proto | xargs sed -e '/^import "google.*/!s/import "/import "schema\//g' -i.bak
docker run -it -v  $(pwd)/iroha-mizuki-cli:/opt/iroha-mizuki-cli mizukisonoko/alpine-grpc-protobuf sh -c  "cd /opt/iroha-mizuki-cli; ls schema/*.proto | xargs -I{} sh -c 'protoc -I=./ --python_out=./ {}; protoc -I=./ --python_out=./ --grpc_out=./ --plugin=protoc-gen-grpc=`which grpc_python_plugin` {}'"
pip install -r requirements.txt 
```

## Env
- Python 3.5.0
- protobuf + grpc [mizukisonoko/alpine-grpc-protobuf](https://github.com/MizukiSonoko/alpine-grpc-protobuf)

## Recover protofile 
```
find schema -type f | sed 'p;s/.bak//' | xargs -n2 mv
```
