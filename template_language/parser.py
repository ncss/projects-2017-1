import re

#possible tokens
#TODO: fix limitation re:matching {}
#TODO: could assign regex to variables
TERMINALS = re.compile('\{\{|\}\}|\{\%|\%\}')
#oops, changed constant
#TOKENS = [re.compile() for token in TOKENS] #list comprehension

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

    def parse(self):
        if self.peek() == '{{':
            node = self._parse_exp()
        elif self.peek() == '{%'
            node = self._parse_tag()
        else:
            node = self._parse_text()
        return node

    def _parse_text(self):
        #TODO: define parent (keep track)
        node = TextNode(None, self.peek())
        self.next()
        return node

    """
    def _parse_exp(self):
        current = node
        expr = self.next()
    """

class Node:
    def __init__(self, parent): #need better variable names
        self.parent = parent

class GroupNode(Node):
    def __init__(self, parent):
        super(GroupNode, self).__init__(parent)
        self.children = []

    def render(self):
        for child in self.children:
            child.render()

class TextNode(Node): #taking in html text --> do nothing
    def __init__(self, parent, text):
        super(TextNode, self).__init__(parent)
        self.text = text

    def render(self):
        print(self.text)


class ExpressionNode(Node): #after {{ --> treat as Python expression
    def __init__(self, parent, expression):
        super(ExpressionNode, self).__init__(parent)
        self.expression = expression

    def render(self):
        print(eval (self.expression))
