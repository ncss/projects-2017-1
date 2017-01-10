import re

#possible tokens
#TODO: fix limitation re:matching {}
#TODO: could assign regex to variables
TERMINALS = re.compile('\{\{|\}\}|\{\%|\%\}')
#oops, changed constant
#TOKENS = [re.compile() for token in TOKENS] #list comprehension

def render_template(template, context):#TODO add
    #TODO template is only a string
    f = open(template).read()
    tokeniser = Tokeniser()
    tokens = tokeniser.tokenise(f)

    parser = Parser(tokens)
    return parser.parse(context)


class Tokeniser:
    def tokenise(self, text):
        tokens = []
        while text:
            match = TERMINALS.search(text) #TOKENS compiled above
            if match:
                start = match.start()
                end = match.end()
                if start != 0:
                    tokens.append(text[:start])
                tokens.append(text[start:end])
                text = text[end:]
            else:
                tokens.append(text)
                text = ''
        return tokens

class Parser:
    def __init__(self, tokens):
        self._tokens = tokens
        self._length = len(tokens)
        self._upto = 0

    def end(self):
        return self._upto >= self._length

    def peek(self):
        return None if self.end() else self._tokens[self._upto]

    def next(self):
        self._upto += 1
        return self.peek()

    def parse(self, context):
        root = self._parse_group()
        return root.render(context)

    def _parse_group(self): #doesn't eat any tokens directly
        node = GroupNode(None) #TODO needs parent
        while not self.end():
            node.children.append(self._parse_components())
        return node

    def _parse_components(self): #doesn't eat any tokens directly
        if self.peek() == '{{':
            node = self._parse_expr()
        elif self.peek() == '{%':
            node = self._parse_tag()
        else:
            node = self._parse_text()
        return node

    def _parse_text(self):
        #TODO: define parent (keep track)
        node = TextNode(None, self.peek())
        self.next() #moves parse to past text
        return node

    def _parse_expr(self):
        current = self.peek()
        expr = self.next()
        close = self.next()
        self.next() #moves parser to past closed token

        #TODO if current != '{{':
            #raise currentError('')

        assert current == '{{', 'Current expected {{'
        assert close == '}}', 'Close expected }}'

        assert expr, 'Expression expected'

        node = ExpressionNode(None, expr) #TODO needs parent
        return node

class Node:
    def __init__(self, parent): #need better variable names
        self.parent = parent

class GroupNode(Node):
    def __init__(self, parent):
        super(GroupNode, self).__init__(parent)
        self.children = []

    def render(self, context):
        return ''.join([child.render(context) for child in self.children])

class TextNode(Node): #taking in html text --> do nothing
    def __init__(self, parent, text):
        super(TextNode, self).__init__(parent)
        self.text = text

    def render(self, context):
        return self.text


class ExpressionNode(Node): #after {{ --> treat as Python expression
    def __init__(self, parent, expression):
        super(ExpressionNode, self).__init__(parent)
        self.expression = expression

    def render(self, context):
        return str(eval (self.expression, {}, context))
