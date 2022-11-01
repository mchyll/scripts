import os


class Token:
    def __str__(self):
        return f"({self.__class__.__name__}, {self._str_value})"
    __repr__ = __str__
class OpenBrace(Token): _str_value = "{"
class CloseBrace(Token): _str_value = "}"
class OpenBracket(Token): _str_value = "["
class CloseBracket(Token): _str_value = "]"
class Separator(Token): _str_value = ","
class Literal(Token):
    def __init__(self, value):
        super().__init__()
        self.value = self._str_value = value


def tokenize(str):
    tokens = []
    pos = 0
    while pos < len(str):
        if str[pos] == "{":
            tokens.append(OpenBrace())
            pos += 1
        elif str[pos] == "}":
            tokens.append(CloseBrace())
            pos += 1
        elif str[pos] == "[":
            tokens.append(OpenBracket())
            pos += 1
        elif str[pos] == "]":
            tokens.append(CloseBracket())
            pos += 1
        elif str[pos] == ",":
            tokens.append(Separator())
            pos += 1
        else:
            literal = ""
            while True:
                if str[pos] == "\\":
                    literal += str[pos+1]
                    pos += 2
                elif str[pos] in "{}[],":
                    break
                else:
                    literal += str[pos]
                    pos += 1
            literal = literal.strip()
            if literal:
                tokens.append(Literal(literal))

    return tokens


def prettyformat(tokens):
    string = ""
    indent = 0
    for token in tokens:
        if isinstance(token, (OpenBrace, OpenBracket)):
            string += "\n" + " " * indent + str(token._str_value) + "\n"
            indent += 4
        elif isinstance(token, (CloseBrace, CloseBracket)):
            indent -= 4
            string += "\n" + " " * indent + str(token._str_value) + "\n"
        elif isinstance(token, Separator):
            string += str(token._str_value) + "\n"
        elif isinstance(token, Literal):
            string += " " * indent + str(token._str_value)
        else:
            raise Exception("Unknown token: " + str(token))

    return string


if __name__ == "__main__":
    base_dir = r"C:\Users\maghyl\OneDrive - Norconsult Group\Documents\D&D"
    with open(os.path.join(base_dir, "adamantine_raw.txt")) as infile, \
        open(os.path.join(base_dir, "adamantine.txt"), "w") as outfile:
        tokens = tokenize(infile.read())
        pretty = prettyformat(tokens)
        outfile.write(pretty)
