# ![logo](./logo_64.png) Iroha Playground


## Test network

```
docker-compose up
```

## Local image

```
docker build -t iroha-playground
docker run -v $(pwd):/usr/src/app --rm -ti iroha-playground poetry run pythone keygen.py --name {KEY_NAME_HERE}
```
