# Marten

[![Build Status](https://travis-ci.org/nick-allen/marten.svg?branch=master)](https://travis-ci.org/nick-allen/marten)
[![Coverage Status](https://coveralls.io/repos/nick-allen/marten/badge.svg?branch=master&service=github)](https://coveralls.io/github/nick-allen/marten?branch=master)

Simple Python configuration management

Inspired by [node config](https://www.npmjs.com/package/config), if you've used it before, Marten will feel familiar
with a couple of extras

Tested with Python 2.7 and 3.5

---


# Install 

`pip install marten`


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

The bundled config is available in python at `marten.config`, and can be accessed like a normal dictionary

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

The configuration files are not parsed, but are fully loaded as python modules

Only capitalized variables not starting with underscores are read into the configuration, leaving everything else for
logic and setup

```
> echo "a = 1; _B = 2; FULL_PYTHON = a + _B == 3" > .marten/python.py
> MARTEN_ENV=python marten
{
    "FULL_PYTHON": true
}
```

## Multiple File Formats

Marten is not tied to a single file format

Currently, it supports Python and JSON, with additional support coming

```
> echo '{"KEY": "value"}' > .marten/formats.json
> MARTEN_ENV=formats marten
{
    "KEY": "value"
}
```

## Environment Variable Replacement

Environment variables in the format `$VAR` are automatically replaced when parsed

Using two `$$` escapes the variable, stripping the first `$`

```
> echo '{"REPLACED": "$ENV", "ESCAPED": "$$ENV"}' > .marten/environ.json
> MARTEN_ENV=environ.json ENV=value marten
{
    "REPLACED": "value",
    "ESCAPED": "$ENV"
}
```

## Merge Multiple Files

Since Marten operates on filename and extension separately, two files with the same name but different extensions
are merged together in the order they are loaded

```
> echo 'PYTHON = True' > .marten/merge.py
> echo '{"JSON": true}' > .marten/merge.json
> MARTEN_ENV=merge marten
{
    "PYTHON": true,
    "JSON": true
}
```

