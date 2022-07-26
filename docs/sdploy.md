# sdploy

sdploy is a tool for helping the deployment of a software stack using the spack
package manager.

sdeploy will create the environment configuration based on the stack definition.
This environment configuration is defined by the following spack configuration
files:

- spack.yaml
- packages.yaml
- modules.yaml
- repos.yaml
- modules.yaml
- mirrors.yaml

sdploy provides the logic to create each one of this files. For this, the user
must provide the list of packages it wants to install in its platform and also
some details about this platform, such as if is accelerated or if it was fast
network support. This is done using the stack file and platform file.

## What is a stack file and how to write it ?

A stack file is the base of sdploy. This is an YAML file in which there will be
defined the compilers to install, major support libraries like MPI, BLAS and
CUDA and the list of packages to install. Of couse, this is a lot of stuff to
process, so a few rules have been taken in to account to make life simpler, both
for the user who will have to write a file that can make several hundred lines
and therfor it can easely make a mistake, but also to sdploy, that needs clear
rules so that the code can be nice to read and to update.

A stack file defines two major components: the programming environment and the
packages to be installed. There can more than one programming file per stack, say
a gcc based programming environment and an intel based programming environment.
Lke wise, it also convinient to have more than one list of packages, we'll see
why in a moment.

## The Programming Environment (PE)

The minimal PE can be seen as just a compiler. Tipically, every stack will have
a programming evironment which will only contain the core compiler and it will
look like this:

    core:
      metadata:
        section: pe
      compiler: gcc@8.5.0

The name of this PE is core because it is used to defined the core compiler or
the system compiler (in other words, the compiler that is insalled by default in
the system). The metadata key is used internally by sdploy and it is used to
group sections with the same functionality (in this case, PE sections).

## Adding packages to the stack

We add a package to the stack by defining a list of packages and including the
package in this list. At the minimum, a list of packages must have the following
structure:

    core:
      metadata:
        section: packages
      pe:
      - gcc_stable
      packages:
      - cmake@3.20.6

`core` is the name of the list of packages (it is a dictionary). The `pe` list
specifies which compilers to use for building the packages in the list. And
`packages` is the actual list of packages. The section key under metadata will
specify that the key core is a list of packages. This will help sdploy to group
all the package lists in a single structure. Remember, if it is a list of
packages, the section key (under metadata) must contain the string packages.

The above declaration will add the following entry to the definitions list:

    definitions:
    - core:
      - cmake@3.20.6

and the following matrix in the specs section:

    specs:
    - matrix:
      - [ $core ]
      - [ $%gcc_stable_compiler ]

Notice that sdploy added `_compiler` to the spec matrix. This is because
gcc\_stable is just a prefix and inside we can find all other packages that make
up the gcc\_stable programming environment, such as the gcc\_stable\_mpi and the
gcc\_stable_blas, which are just tokens for the MPI and BLAS libraries defined
in the PE. See more of this in the PE section above.

If we would like to compile the core packages list with the intel compiler too,
we would simply add the intel programming environment to the `pe` list. In that
case, the core package list would look like this:

    core:
      metadata:
        section: packages
      pe:
      - gcc_stable
      - intel_stable
      packages:
      - cmake@3.20.6

And the corresponding spec would become:

    - matrix:
      - [ $core ]
      - [ $%gcc_stable_compiler ]
    - matrix:
      - [ $core ]
      - [ $%intel_stable_compiler ]

Notice that we didn't change the list of packages itself, we are still compiling
a single package, cmake@3.20.6.

Now let's move on to a package that requires MPI support. For this we are going
to create a new list of packages and we are going to name it `mpi_pkgs`. It is a
good pratice to come up with names that can give a hint on what kind of packages
is this list made of:

    mpi_pkgs:
      metadata:
        section: packages
      pe:
      - gcc_stable
      dependencies:
      - mpi
      packages:
      - fftw+mpi

As expected, the definitions list is straightforward:

    - mpi_pkgs:
      - fftw+mpi

But now the specs list has an extra line which will make spack to compile fftw
with the MPI library specified in the programming environment gcc_stable.

    - matrix:
      - [ $mpi_pkgs ]
      - [ $^gcc_stable_mpi ]
      - [ $%gcc_stable_compiler ]

Ia a package needs more dependencies to compile, they just need to be added to
dependencies key where the package is defined. For example, hypre can be such a
case, so we give a last example using this package. We will create a new list of
packages for this example and we will call it mpi\_blas\_cuda_pkgs:

    mpi_blas_cuda_pkgs:
      metadata:
        section: packages
      pe:
      - gcc_stable
      dependencies:
      - mpi
      - blas
      - cuda
      packages:
      - hypre+mpi+blas+cuda

For the mpi_blas_cuda_pkgs list of packages just defined, the specs matrix would
become like this:

    - matrix:
      - [ $mpi_pkgs ]
      - [ $^gcc_stable_mpi ]
      - [ $^gcc_stable_blas ]
      - [ $^gcc_stable_cuda ]
      - [ $%gcc_stable_compiler ]

## Default packages

Spack allows you to customize how your software is built through the
packages.yaml file. To specify a default package we add the default key in the
package spec:

## Filters

This is a way to enable the same stack definition to work across different
platforms.

A filter is defined in the platform file under the section filters. Many filters
can be defined for the same platform.

Neither a filter key nor its value can have the name none.

## Tokens

A token is just a replacement place for a name that have been defined earlier.
This will enable, for example, that we can read which is the core compilers
defined for the platform and then use it across the stack, where needed.

A token is defined in the platform file under the section tokens. Many tokens
can be defined fo the same platform.

## Concepts

In this section we give some details about the specific terminology used by
sdploy and how to use them.

### Programming Environment

A programming environment is the set of software that will enable the
compilation of all other packages and provides the necessary dependencies for
using the hardware in its full potential, such as CUDA libraries, MPI libraries,
a modern Python implementation and possibly even other tools.

## Reserved words

filters
tokens
pe
metadata
section



