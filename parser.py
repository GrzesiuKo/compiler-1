from projekt.tokens import Token


class Parser:

    ##### Parser header #####
    def __init__(self, scanner):
        self.next_token = scanner.next_token
        self.token = self.next_token()

    def take_token(self, token_type):
        if self.token.type != token_type:
            self.error("Unexpected token: %s" % token_type)
        if token_type != 'EOF':
            self.token = self.next_token()

    def error(self, msg):
        raise RuntimeError('Parser error, %s' % msg)

    """ Gramatyka BNF
    
        <services> ::= 'services'
        <version> ::= 'version'
        <networks> ::= 'networks'
        <volumes> ::= 'volumes'
        <build> ::= 'build'
        <ports> ::= 'ports'
        <image> ::= 'image'
        <environment> ::= 'environment'
        <deploy> ::= 'deploy'
        <number> ::= r'\d+(\.\d*)?'
        <id> ::= r'[A-Za-z_./-]+'
        <string> ::= r'\"(.*?)\"'
        <assign> ::= ':'
        <item> ::= '-'
        <eof> ::= end of file
        
        
        <start> ::= <program> <eof>
        <program> ::= <statement> <program>
        <program> ::= <statement>
        <statement> ::= <version_stmt> | <services_stmt> | <networks_stmt> | <volumes_stmt>
        <version_stmt> ::= <version> <assign> <string>
        <services_stmt> ::= <services><assign><service>
        <service> ::= <string><assign><element><service>
        <service> ::= <string><assign><element><services_stmt>
        <service> ::= <string><assign><element><eof>
        <element> ::= <string><assign><string>
        <element> ::= <string><assign><number>
        <element> ::= <string><assign><array>
        <element> ::= <string><assign><element>
        <array> ::= <item><string>
        <array> ::= <item><string><array>
        
        """

    ##### Parser body #####


    # Starting symbol
    def start(self):
        # start -> program EOF
        if self.token.type in Token.START_TOKENS:
            self.program()
            self.take_token('EOF')
        else:
            self.error("Epsilon not allowed")

    def program(self):
        # program -> statement program
        if self.token.type in Token.STATEMENTS:
            self.statement()
            self.program()
        # program -> eps
        else:
            pass

    def statement(self):
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
        if self.token.type == Token.VERSION:
            self.take_token(Token.VERSION)
            self.take_token(Token.ASSIGN)
            self.take_token(Token.STRING)
            print("version_stmt OK")
        else:
            self.error("Epsilon not allowed")

    # assign_stmt -> ID ASSIGN value END
    def services_stmt(self):
        if self.token.type == 'ID':
            self.take_token('ID')
            self.take_token('ASSIGN')
            self.value()
            self.take_token('END')
            print("assign_stmt OK")
        else:
            self.error("Epsilon not allowed")

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
