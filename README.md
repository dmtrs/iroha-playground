# Iroha <img height="24px;" src="logo.svg" alt="Iroha Playground" /> Playground

Hyperldeger Iroha test network setup as a Playground. 
See: [hyperledger/iroha](https://github.com/hyperledger/iroha)

## Test network

```
docker-compose up
```

## Local image

```
docker build -t iroha-playground
docker run -v $(pwd):/usr/src/app --rm -ti iroha-playground poetry run pythone keygen.py --name {KEY_NAME_HERE}
```

### Misc
- [iconset](https://www.iconfinder.com/iconsets/kid-playground-and-toys)
