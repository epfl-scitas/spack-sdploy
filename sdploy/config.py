# GENERAL DEFINITIONS #######################################################
#
#
CONFIG_FILE = 'config/sdploy.yaml'
SEP = '/'
OPEN_TOKEN = '<'
CLOSE_TOKEN = '>'
# SCHEMA DEFINITIONS ########################################################
#
#
#   PKG_LIST_NAME:
#     SD_METADATA_KEY:
#       SD_METADATA_SECTION_KEY: <name_of_section>
#     SD_PE:
#     - <name_of_pe_1>
#     - <name_of_pe_2>
#     - ...
#     SD_PACKAGES:
#     - <name_of_package_1>
#
#
SD_METADATA_KEY = 'metadata'
SD_METADATA_SECTION_KEY = 'section'
SD_PE_KEY = 'pe'
SD_PACKAGES_KEY = 'packages'
SD_DEPENDENCIES_KEY = 'dependencies'
SD_PACKAGES_YAML_KEY = 'default'
SD_MODULES_YAML_KEY = 'modules'
