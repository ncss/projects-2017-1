import re

#possible tokens
#TODO: fix limitation re:matching {}
#TODO: could assign regex to variables
TERMINALS = re.compile('\{\{|\}\}|\{\%|\%\}')
#oops, changed constant
#TOKENS = [re.compile() for token in TOKENS] #list comprehension
TEMPLATES_PATH = 'templates'

def render_template(template, context):#TODO add
    parser = Parser(Tokeniser.tokenise(template))
    return parser.parse(context)

class Tokeniser:
    @staticmethod
    def tokenise(filename):
        with open(TEMPLATES_PATH + '/' + filename) as f: #TODO fix path
            text = f.read()
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

    def _parse_tag(self):
        tag = self.next()
        match = re.match(r'^\s*include\s+(\S+)\s*$', tag)
        if match:
            path = match.group(1)
            p = Parser(Tokeniser.tokenise(path))
            assert self.next() == '%}', 'Close expected %}'
            self.next()
            return p._parse_group()
        match = re.match(r'^\s*if\s+(\S.*)', tag)
        if match:
            return self._parse_simple_if()
        match = re.match(r'^\s*for\s+(\S.*)', tag)
        if match:
            return self._parse_simple_for()
        assert False, 'Tag not recognised'

    def _parse_simple_if(self):
        predicate = self.peek()
        close = self.next()

        assert close == '%}', 'Close expected %}'

        match = re.match(r'^\s*if\s+(\S.*)', predicate)
        if match:
            predicate = match.group(1)
            tokens = []
            while self.next() not in ['{%', '%}']:
                tokens.append(self.peek())
            if eval(predicate):
                p = Parser(tokens)
                node = p._parse_group()
            else:
                node = TextNode(None, '')

            open_end_if = self.peek()
            end_if = self.next()
            close_end_if = self.next()
            self.next()

            assert open_end_if == '{%', 'Open expected {%'
            assert end_if.strip() == 'end if', 'End if expected'
            assert close_end_if == '%}', 'Close expected %}'

            return node

        assert False, 'If statement not recognised'

    def _parse_simple_for(self):
        argument = self.peek()
        close = self.next()

        assert close == '%}', 'Close expected %}'

        match = re.match(r'^\s*for\s+(\S+)\s+in\s+(\S+)\s*$', argument)
        if match:
            variable = match.group(1)
            expression = match.group(2)
            tokens = []
            while self.next() not in ['{%', '%}']: #control block
                tokens.append(self.peek())
            p = Parser(tokens)
            node = p._parse_group()
            for_node = ForNode(None, variable, expression, node)
            open_end_for = self.peek()
            end_for = self.next()
            close_end_for = self.next()
            self.next()

            assert open_end_for == '{%', 'Open expected {%'
            assert end_for.strip() == 'end for', 'End for expected'
            assert close_end_for == '%}', 'Close expected %}'

            return for_node

        assert False, 'For statement not recognised'



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

class ForNode(Node):
    def __init__(self, parent, variable, expression, group_node):
        super(ForNode, self).__init__(parent)
        self.variable = variable
        self.expression = expression
        self.group_node = group_node

    def render (self, context):
        for_list = []
        for element in eval(self.expression, {}, context):
            context[self.variable] = element
            for_list.append(self.group_node.render(context)) #TODO security vulnerability?
        return ''.join(for_list)


class IfNode(Node):
    def __init__(self, parent):
        super(IfNode, self).__init__(parent)
        self.predicate = predicate


if __name__ == '__main__':
    TEMPLATES_PATH = 'template_language\\test_templates'
    print("====")
    print(render_template('test.txt', {'d': 'username'}))
    print("====")
    print(render_template('test2.txt', {'d': 'username'}))
    print("====")
    print(render_template('simpleiftest.txt', {'d': 'username'}))
    print("====")
    print(render_template('simplefortest.txt', {'b': ['abc', 'def']}))
    print("====")
