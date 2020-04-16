try:
    from Akoma.tokenizer.TokenType import TokenType
except ModuleNotFoundError:
    try:
        from tokenizer.TokenType import TokenType
    except ModuleNotFoundError:
        print("Error")
        exit(-1)


class BasicReasoner():
    def __init__(self, tokenizer, akomabuilder):
        self.tokenizer = tokenizer
        self.akomabuilder = akomabuilder
        self.current_token = False
        self.current_hierarchy = {
            TokenType.DEO: 0,
            TokenType.GLAVA: 0,
            TokenType.ODELJAK: 0,
            TokenType.PODODELJAK: 0,
            TokenType.CLAN: 0,
            TokenType.STAV: 0,
            TokenType.TACKA: 0,
            TokenType.PODTACKA: 0,
            TokenType.ALINEJA: 0}

    def start(self):
        body = False
        preface = []
        while self.current_token is not None:
            self.current_token = self.tokenizer.get_next_token()

            if(self.current_token is None):
                break
            if body is False and self.current_token.type <= TokenType.CLAN :
                body = True
                self.akomabuilder.build_preface(preface)
            else:
                preface.append(self.current_token)
            if body:
                self.reason(0)

    def reason(self,sanity):

        if self.current_token is None:
            return
        if self.current_token.type == TokenType.DEO and self.current_token.value == None:
            self.deo_glava_find_title()
        elif self.current_token.type == TokenType.GLAVA and self.current_token.value == None:
            self.deo_glava_find_title(sanity + 1)
        elif self.current_token.type == TokenType.STAV and self.current_token.value[-1:] != "." and self.current_token.value[-1:] != ":"and self.current_token.value[-1:] != "," and sanity < 10:
            self.title_find_clan()
        else:
            self.akomabuilder.add_token(self.current_token, self.get_identification(self.current_token))
            if self.current_token.type == TokenType.STAV and self.current_token.value[-1:] == ":" and sanity < 10:
                sanity = sanity + 2
                self.expect_tacke(sanity)
            # elif sanity >= 10:
                # print(str(self.current_token.type) + "ID=" + str(self.current_token.numberstr)  +"  VREDNOST:" +  str(self.current_token.value)) #TODO FIX ERROR (QUICKFIX FOR INFI LOOP)

    def deo_glava_find_title(self,sanity):
        glava = self.current_token
        self.current_token = self.tokenizer.get_next_token()
        if (self.current_token.type != TokenType.STAV):
            print("WARNING - GLAVA NEMA NASLOV")
            self.akomabuilder.add_token(glava, self.get_identification(glava))
            self.reason(sanity)
        elif (self.current_token.value[-1:] == "."):
            print("WARNING - NASLOV GLAVE NE SME DA IMA TACKU NA KRAJU")
            self.akomabuilder.add_token(glava, self.get_identification(glava))
            self.reason(sanity)
        else:
            glava.value = self.current_token.value
            self.akomabuilder.add_token(glava, self.get_identification(glava))
        #self.reason()

    def title_find_clan(self):
        naslov = self.current_token
        self.current_token = self.tokenizer.get_next_token()
        if self.current_token is None:
            return
        if self.current_token.type != TokenType.CLAN:
            print("WARNING - NEMA CLANA ISPOD NASLOVA")
            self.akomabuilder.add_token(naslov, self.get_identification(naslov))
            self.reason(0) # deal with this unknown element
            print(self.current_hierarchy)
            print(naslov.value)
        else:
            self.current_token.value = naslov.value
            self.akomabuilder.add_token(self.current_token, self.get_identification(self.current_token))

    def expect_tacke(self, sanity):
        #print("TACKA?")
        while self.current_token is not None:
            self.current_token = self.tokenizer.get_next_token()
            if(self.current_token is None):
                break
            elif self.current_token.type == TokenType.ODELJAK:
                if (self.current_token.type == TokenType.ODELJAK):
                    self.current_token.type = TokenType.TACKA
                    self.current_token.name = "тачка"
                self.reason(sanity)
           # elif self.current_token.type <= TokenType.STAV:
           #     self.reason()
            elif sanity < 10:
                self.reason(sanity)

    def get_identification(self, token):
        if token.number is None:
            self.current_hierarchy[token.type] += 1
        elif token.number2 is not None :
            self.current_hierarchy[token.type] = token.number2
        else:
            self.current_hierarchy[token.type] = token.number

        for i in range(TokenType.ALINEJA, token.type, -1):
            if i == TokenType.CLAN:
                continue
            self.current_hierarchy[i] = 0

        #if token.type+1 != TokenType.CLAN and token.type != TokenType.ALINEJA:
         #   self.current_hierarchy[token.type+1] = 0

        values = ["deo","gla", "od", "podod", "clan", "stav", "tac", "podtac", "ali"]
        retval = ""
        for i in range(TokenType.DEO, TokenType.ALINEJA+1):
            if token.type < i:
                break
            if self.current_hierarchy[i] == 0:
                continue

            retval += values[i] + str(self.current_hierarchy[i]) + "-"

        return retval[:-1]

