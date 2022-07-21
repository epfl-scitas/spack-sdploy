# spack-sdploy
Spack extension for automatic package configuration and deployment

## How to install

+ Source your local python environment
+ Source `spack`
+ Install `sdploy` dependencies
+ configure the extension in spack config.yaml
+ execute `spack -h` to check that is working

## write-spack-yaml

```
spack write-spack-yaml -s samples/stack.yaml -tp templates -tf spack.yaml.j2
```
If no options are specified, it will look for the files in the current directory.
