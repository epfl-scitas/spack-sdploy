def setup_parser(subparser):
    # spack-sdploy will look for a stack after the name given in the parameter
    # stack under the stacks directory. If it doesn't find, it will assume that
    # the parameter stack is a fully qualified file name to a stack.yaml file.
    subparser.add_argument(
        '-s', '--stack',
        help='path to the stack file'
    )
    subparser.add_argument(
        '-p', '--platform',
        help='path to the platform file.'
    )
    subparser.add_argument(
        '--prefix', type=str,
        help='path to the stacks directory.'
    )
    subparser.add_argument(
        '-w', '--work_directory', type=str,
        help='path to overwrite work  directory.'
    )
    subparser.add_argument(
        '-d', '--debug', action='store_true', default=False,
        help='print debug information.'
   )
