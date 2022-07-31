# spack-sdploy

Spack extension for automatic package configuration and deployment.

## How to install

You can try out this Spack extension be executing 4 easy steps:

+ Set up and activate a local python environment
+ Set up and activate `spack`
+ Install `spack-sdploy` dependencies
+ Clone and configure spack-sdploy

This 4 steps are now detailed in the next section.

### Step-by-step installation

Just for a matter of completeness, all the steps needed get up and running with
spack-sdploy extension will be covered, which can be a bit pedantic.

#### Set up and activate a local python environment

It is recommended that a Python environment be used to support sdploy. This same
Python can also be used to run Spack.

    python3 -m venv <path-to-environment-directory>
    . <path-to-environment-directory>/bin/activate
    
For more information on how to create a virtual environment in Python refer to
the PEP 405 – Python Virtual Environments documentation.

#### Set up and activate Spack

See the
[Spack documentation](https://spack.readthedocs.io/en/latest/getting_started.html#installation)
on how to install Spack. For sake of completeness, we copy paste the commands here:

    git clone -c feature.manyFiles=true https://github.com/spack/spack.git
    . spack/share/spack/setup-env.sh

#### Install `spack-sdploy` dependencies

Up to now the only dependency of spack-sdploy if jinja2. Once you have activated
Python environment, you can simply use pip to install the packages.

    pip install jinja2

#### Clone and configure spack-sdploy

    git clone git@github.com:epfl-scitas/spack-sdploy

To activate the spack-sdploy extension you must add it to the config.yaml. If
you already have another Spack installation and just want to try out
spack-sdploy may very well create a temporary directory to store the
configuration and then use the SPACK_USER_CONFIG_PATH variable to point this new
directory.

    mkdir temporary_config
    export SPACK_USER_CONFIG_PATH=/path/to/temporary_config

and then, inside the temporary_config directory, write a config.yaml file with
the following contents:

    config:
      extensions:
      - /path/to/spack-sdploy
      
Be sure you do not change the spack-dploy directory. Spack forces the extensions
to follow strict rules. Please see the
[Spack Extensions](https://spack.readthedocs.io/en/latest/extensions.html)
documentation for more details about this subject. At this point you should now
be able to call `spack -h` and see the new Spack commands deployed by the
spack-sdploy extension.

## How to use

At the present time, spack-sdploy will add 2 commands to your already existing
Spack commands. These commandes are:

    spack write-spack-yaml
    spack write-packages-yaml

In the future we may change the names of these commands, but for now lets just
imagine these are short and easy to type commands.

As you may have guessed it (if you haven't that's ok), write-spack-yaml will
write the spack.yaml file and write-packages-yaml will write the packages.yaml
file. Of course, Spack does not (yet!) guess what you may want to install and
for that purpose, both these commands will read all the specs you want in your
spack.yaml file by reading another file you have previously written and which
we call by stack.yaml.

For the time being, spack-sdploy already comes with a dummy stack.yaml so we can
get started using the new commands.

## write-spack-yaml

```
spack write-spack-yaml -s samples/stack.yaml -tp templates -tf spack.yaml.j2
```
If no options are specified, it will look for the files in the current directory.
