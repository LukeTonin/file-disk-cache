# File Disk Cache

This is an extension of the [DiskCache](https://github.com/grantjenks/python-diskcache) package.

It extends the functionality of the original disk cache package by allowing users to store objects as different file types within the cache.

This might be useful is one interested in keeping a human interpretable file structure within their file cache.

## Installation

### Install from source

This method is useful if you want to have the packages installed while developing them and make use of pip's "editable" installs (i.e the ability to change code dynamically without reinstalling.)

Clone the repository from github and install it from source.
```
pip install --editable /path/to/file-disk-cache
```

## Releasing

The package follows [semantic versioning](https://semver.org). To create a new versioned release of `File Disk Cache`:

1. Update the version in the pyproject file (e.g. for a minor bump update the second number). 

2. Once the change has been merged, switch to the `main` locally and create a new git tag. (Make sure the tag is
   annotated) e.g.

```
git tag -a v1.1.3 -m "release notes here"
```

3. Push the tag to GitHub

```sh
git push origin --tags
```


## Testing

To test this repository, call:
```
make test
```

This action is defined in the [Makefile](./Makefile)