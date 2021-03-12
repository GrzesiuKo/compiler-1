from projekt.tokens import Token


class Parser:

    ##### Parser header #####
    def __init__(self, scanner):
        self.next_token = scanner.next_token
        self.token = self.next_token()

    def take_token(self, token_type):
        if self.token.type != token_type:
            self.error(
                "Unexpected token: " + token_type + " Expected: " + self.token.type + " Line: " + str(self.token.line)
                +" Value: "+self.token.value)
        if token_type != 'EOF':
            self.token = self.next_token()

        # print("Token: "+token_type+" value: "+self.token.value)

    def error(self, msg):
        raise RuntimeError('Parser error, ' + msg)

    ##### Parser body #####

    # Starting symbol
    def start(self):
        print("start")
        # start -> program EOF
        if self.token.type in Token.START_TOKENS:
            self.program()
            self.take_token('EOF')
        else:
            self.error("Epsilon not allowed")

    def program(self):
        print("program value: '"+self.token.value+"'")
        # program -> statement program
        if self.token.type in Token.STATEMENTS:
            self.statement()
            self.program()
        # program -> eps
        else:
            print("ETF: "+self.token.value)
            pass

    def statement(self):
        print("statement")
        if self.token.type == Token.VERSION:
            self.version_stmt()
        elif self.token.type == Token.SERVICES:
            self.services_stmt()
        elif self.token.type == Token.NETWORKS:
            self.networks_stmt()
        elif self.token.type == Token.VOLUMES:
            self.volumes_stmt()
        else:
            self.error("Epsilon not allowed")

    def version_stmt(self):
        print("version_stmt")
        if self.token.type == Token.VERSION:
            self.take_token(Token.VERSION)
            self.take_token(Token.ASSIGN)
            self.take_token(Token.STRING)
            print("version_stmt OK")
        else:
            self.error("Epsilon not allowed")

    def services_stmt(self):
        print("services_stmt")
        if self.token.type == Token.SERVICES:
            self.take_token(Token.SERVICES)
            self.take_token(Token.ASSIGN)
            self.service()
            print("services_stmt OK")
        else:
            self.error("Epsilon not allowed")

    def service(self):
        print("service token: "+self.token.type+" "+self.token.value)
        if self.token.type == Token.ID:
            self.take_token(Token.ID)
            self.take_token(Token.ASSIGN)
            self.element()

            print("service OK")
        else:
            pass

    def element(self):
        print("element token: "+self.token.type+" "+self.token.value)
        start, service_name, indent = self.token.line, self.token.value, self.token.column
        elements = {Token.PORTS: self.ports_stmt,
                    Token.BUILD: self.build_stmt,
                    Token.IMAGE: self.image_stmt,
                    Token.ENVIRONMENT: self.environment_stmt,
                    Token.DEPLOY: self.deploy_stmt,
                    Token.NETWORKS: self.networks,
                    Token.VOLUMES: self.volumes}
        if self.token.type in elements:
            elements[self.token.type]()
            self.element()
        elif self.token.column == indent:
            self.service()

        else:
            self.error("Epsilon not allowed")

    def ports_stmt(self):
        print("ports token: " + self.token.type + " " + self.token.value)
        if self.token.type == Token.PORTS:
            self.take_token(Token.PORTS)
            self.take_token(Token.ASSIGN)
            self.list()
        else:
            self.error("Epsilon not allowed")

    def list(self):
        print("list token: " + self.token.type + " " + self.token.value)
        if self.token.type == Token.ITEM:
            self.take_token(Token.ITEM)
            self.take_token(Token.ID)
            self.list()
        else:
            pass

    def build_stmt(self):
        if self.token.type == Token.BUILD:
            self.take_token(Token.BUILD)
            self.take_token(Token.ASSIGN)
            self.take_token(Token.STRING)
        else:
            pass

    def image_stmt(self):
        print("image")
        if self.token.type == Token.IMAGE:
            self.take_token(Token.IMAGE)
            self.take_token(Token.ASSIGN)
            self.take_token(Token.ID)
            print("end image  token: "+self.token.type+" "+self.token.value)
        else:
            pass

    def environment_stmt(self):
        if self.token.type == Token.ENVIRONMENT:
            self.take_token(Token.ENVIRONMENT)
            self.take_token(Token.ASSIGN)
            self.dict()
        else:
            pass

    def dict(self):
        if self.token.type == Token.STRING:
            self.take_token(Token.STRING)
            self.take_token(Token.ASSIGN)
            self.take_token(Token.STRING)
            self.dict()
        else:
            pass

    def deploy_stmt(self):
        if self.token.type == Token.DEPLOY:
            self.take_token(Token.DEPLOY)
            self.take_token(Token.ASSIGN)
            self.dict()
        else:
            pass

    def networks(self):
        if self.token.type == Token.NETWORKS:
            self.take_token(Token.NETWORKS)
            self.take_token(Token.ASSIGN)
            self.list()
        else:
            pass

    def volumes(self):
        if self.token.type == Token.VOLUMES:
            self.take_token(Token.VOLUMES)
            self.take_token(Token.ASSIGN)
            self.list()
        else:
            pass

    def networks_stmt(self):
        # value -> NUMBER
        if self.token.type == 'NUMBER':
            self.take_token('NUMBER')
        # value -> ID
        elif self.token.type == 'ID':
            self.take_token('ID')
        else:
            self.error("Epsilon not allowed")

    def volumes_stmt(self):
        # if_stmt -> IF ID THEN program ENDIF END
        if self.token.type == 'IF':
            self.take_token('IF')
            self.take_token('ID')
            self.take_token('THEN')
            self.program()
            self.take_token('ENDIF')
            self.take_token('END')
            print("if_stmt OK")
        else:
            self.error("Epsilon not allowed")
