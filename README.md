# Marten

[![Build Status](https://travis-ci.org/nick-allen/marten.svg?branch=master)](https://travis-ci.org/nick-allen/marten)
[![Coverage Status](https://coveralls.io/repos/nick-allen/marten/badge.svg?branch=master&service=github)](https://coveralls.io/github/nick-allen/marten?branch=master)
[![PyPI version](https://badge.fury.io/py/marten.svg)](https://badge.fury.io/py/marten) 

Stupid simple Python configuration environments

Inspired by [node config](https://www.npmjs.com/package/config), if you've used it before, Marten will feel familiar
with a couple of extras

Tested with Python 2.7 and 3.5

---


# Install 

```
> pip install marten
```


# Usage

Marten provides several ways to load configurations, the simplest being the bundled config automatically
created by Marten using files found in the `.marten/` directory

```
> mkdir .marten
> echo "EXAMPLE = True" > .marten/default.py
> marten
{
    "EXAMPLE": true
}
```

The `marten` command outputs the fully parsed content of the bundled Marten config in JSON format

The bundled config is available in Python at `marten.config`, and can be accessed like a normal dictionary

```
> python
>>> from marten import config
>>> config['EXAMPLE']
True
```


# Features


## Swappable Configurations

Marten can easily swap between different configurations using the `MARTEN_ENV` environment variable

The `MARTEN_ENV` variable defaults to `default` 

```
> marten
{
    "EXAMPLE": true
}
> echo "SECOND_FILE = 'This is a different environment'" > .marten/two.py
> echo "THIRD_FILE = 'This is a third environment'" > .marten/three.py
> MARTEN_ENV=two marten
{
    "SECOND_FILE": "This is a different environment"
}
> MARTEN_ENV=three marten
{
    "THIRD_FILE": "This is a third environment"
}
```


## Full Python

The configuration files are not parsed, but are imported as Python modules

Only capitalized variables not starting with underscores are read into the configuration, allowing other variables
to be used for logic and setup

```
> echo "a = 1; _B = 2; FULL_PYTHON = a + _B == 3" > .marten/python.py
> MARTEN_ENV=python marten
{
    "FULL_PYTHON": true
}
```


## Multiple File Formats

Marten is not limited to Python files

```
> echo '{"KEY": "value"}' > .marten/formats.json
> MARTEN_ENV=formats marten
{
    "KEY": "value"
}
```

Current supported formats:

* Python
* JSON
* YAML


## Environment Variable Expansion

Environment variables in values with the format `$VAR` or `${VAR}` are automatically expanded

Unset environment variables are unmodified

```
> echo '{"REPLACED1": "This ${ENV}", "REPLACED2": "Second $ENV", "IGNORED": "${MISSING}"}' > .marten/environ.json
> MARTEN_ENV=environ ENV=value marten
{
    "IGNORED": "${MISSING}",
    "REPLACED1": "This value",
    "REPLACED2": "Second value"
}
```


## Merge Multiple Files

Since Marten operates on filename and extension separately, two files with the same name but different extensions
are merged together in the order they are loaded

```
> echo 'PYTHON = True' > .marten/merge.py
> echo '{"JSON": true}' > .marten/merge.json
> echo 'YAML: true' > .marten/merge.yaml
> MARTEN_ENV=merge marten
{
    "JSON": true,
    "PYTHON": true,
    "YAML": true
}
```


# License

Available under the MIT license

See LICENSE for more details
