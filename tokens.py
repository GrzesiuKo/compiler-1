class Token:
    SERVICES = 'services'
    VERSION = 'version'
    NETWORKS = 'networks'
    VOLUMES = 'volumes'
    BUILD = 'build'
    PORTS = 'ports'
    IMAGE = 'image'
    ENVIRONMENT = 'environment'
    DEPLOY = 'deploy'

    START_TOKENS = [VERSION, 'EOF']
    STATEMENTS = [VERSION, SERVICES, NETWORKS, VOLUMES]

    ASSIGN = 'assign'
    STRING = 'string'

    NUMBER = "number"
    ID = "id"
    ITEM = "item"
    NEWLINE = "newline"
    SKIP = "SKIP"
