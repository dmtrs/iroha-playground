<h1 align="center">
    <strong>Iroha<img height="24px;" src="logo.svg" alt="Iroha Playground" /> Playground</strong>
</h1>
<p align="center">
    <a href="https://github.com/dmtrs/iroha-playground" target="_blank">
        <img src="https://img.shields.io/github/last-commit/dmtrs/iroha-playground" alt="Latest Commit">
    </a>
        <img src="https://img.shields.io/github/workflow/status/dmtrs/iroha-playground/Test">
        <img src="https://img.shields.io/codecov/c/github/dmtrs/iroha-playground">
    <br />
    <img src="https://img.shields.io/github/license/dmtrs/iroha-playground">
</p>

Hyperldeger Iroha test network setup as a Playground. 
See: [hyperledger/iroha](https://github.com/hyperledger/iroha)

## Bootstrap

```
docker-compose up --detach
```

Graphql server under: `http://localhost:8000`

## Local image

```
docker build -t iroha-playground
docker run -v $(pwd):/usr/src/app --rm -ti iroha-playground poetry run python keygen.py --name {KEY_NAME_HERE}
docker run -v $(pwd):/usr/src/app --rm -ti iroha-playground poetry run ptw -- --mypy playground --cov=playground --cov-report=term-missing:skip-covered --cov-report=xml tests/unit
```

### Misc
- [iconset](https://www.iconfinder.com/iconsets/kid-playground-and-toys)
