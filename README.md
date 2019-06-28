# python-cpsk-api ![travis](https://travis-ci.org/Adman/python-cpsk-api.svg?branch=master)

Simple python api for grabbing data from cp.sk

## Installation

Available on [pypi](https://pypi.org/project/cpsk/)

Running `$ pip install cpsk` will get the package installed

## Usage

```python
import cpsk
drive = cpsk.get_routes('Bratislava', 'Praha', **kwargs)
```

### Available kwargs

| parameter | type    | description                                                                        |
| --------- | ------- | ---------------------------------------------------------------------------------- |
| `vehicle` | string  | Vehicle to travel with. Default `vlakbus`. Available: `vlak`, `bus`, `vlakbusmhd`. |
| `time`    | string  | Departure time. Defaults to current time.                                          |
| `date`    | string  | Departure date. Defaults to current date.                                          |
| `direct`  | boolean | Whether to look only for direct routes. Defaults to `False`.                       |


*Beware that by using this you might be violating cp.sk ToS*
