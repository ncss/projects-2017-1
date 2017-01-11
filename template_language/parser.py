import re
import html

#possible tokens
#TODO: fix limitation re:matching {}
#TODO: could assign regex to variables
TERMINALS = re.compile('\{\{|\}\}|\{\%|\%\}')
#oops, changed constant
#TOKENS = [re.compile() for token in TOKENS] #list comprehension
TEMPLATES_PATH = 'templates'

def render_template(template, context):#TODO add
    parser = Parser(Tokeniser.tokenise(template))
    return parser.parse().render(context)

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

    def parse(self):
        root = GroupNode()
        self._parse(root, None)
        return root

    def _parse(self, parent, parent_tag):
        while not self.end():
            if self.peek() == '{{':
                parent.children.append(self._parse_expr())
            elif self.peek() == '{%':
                tag = self.next()
                match = re.match(r'^\s*(\S+)\s*(.*)$', tag)
                assert match, 'no argument to {%'
                tag = match.group(1)
                argument = match.group(2)
                assert self.next() == '%}', 'No close %} tag'
                self.next()

                if tag == 'include':
                    p = Parser(Tokeniser.tokenise(argument.strip()))
                    node = p.parse()
                    parent.children.append(node)

                if tag == 'let':
                    group_node = GroupNode()
                    match = re.match(r'^\s*(\S+)\s*=\s*(.*)$', argument)
                    variable = match.group(1)
                    expression = match.group(2)
                    assignment_node = AssignmentNode(variable, expression)
                    parent.children.append(assignment_node)

                if tag == 'if':
                    group_node = GroupNode()
                    node = IfNode(argument, group_node)
                    self._parse(group_node, 'if')
                    parent.children.append(node)

                if tag == 'for':
                    group_node = GroupNode()
                    match = re.match(r'^\s*(\S+)\s+in\s+(.*)$', argument)
                    variable = match.group(1)
                    expression = match.group(2)
                    node = ForNode(variable, expression, group_node)
                    self._parse(group_node, 'for')
                    parent.children.append(node)

                if tag == 'comment':
                    group_node = GroupNode()
                    self._parse(group_node,'comment')
                    ## Parse through a comment and not append to parent

                if tag == 'end':
                    assert argument.strip() == parent_tag, 'close tag does not match open tag'
                    return
            else:
                parent.children.append(self._parse_text())

        assert parent_tag == None, 'Still have open tag at end of template'
        return

    def _parse_text(self):
        node = TextNode(self.peek())
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

        node = ExpressionNode(expr)
        return node

class Node:
    def __init__(self): #need better variable names
        pass

class GroupNode(Node):
    def __init__(self):
        super(GroupNode, self).__init__()
        self.children = []

    def render(self, context):
        return ''.join([child.render(context) for child in self.children])

class TextNode(Node): #taking in html text --> do nothing
    def __init__(self, text):
        super(TextNode, self).__init__()
        self.text = text

    def render(self, context):
        return self.text

class ExpressionNode(Node): #after {{ --> treat as Python expression
    def __init__(self, expression):
        super(ExpressionNode, self).__init__()
        self.expression = expression

    def render(self, context):
        safe = re.match(r'^\s*safe\s+(.*)$', self.expression)
        if safe:
            return str(eval(safe.group(1), {}, context))
        else:
            return html.escape(str(eval(self.expression, {}, context)))

class AssignmentNode(Node):
    def __init__(self, variable, expression):
        super(AssignmentNode, self).__init__()
        self.variable = variable
        self.expression = expression

    def render(self, context):
        context[self.variable] = eval(self.expression) #dictionary index with key
        return ''

class ForNode(Node):
    def __init__(self, variable, expression, group_node):
        super(ForNode, self).__init__()
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
    def __init__(self, predicate, group_node):
        super(IfNode, self).__init__()
        self.predicate = predicate
        self.group_node = group_node

    def render(self, context):
        if eval(self.predicate, {}, context):
            result = self.group_node.render(context)
            return result
        return ''

if __name__ == '__main__':
    TEMPLATES_PATH = 'test_templates'
    print("====")
    print(render_template('test.txt', {'d': '<<<<username'}))
    print("====")
    print(render_template('test2.txt', {'d': 'username'}))
    print("====")
    print(render_template('simpleiftest.txt', {'d': 'username'}))
    print("====")
    print(render_template('simplefortest.txt', {'b': ['abc', 'def']}))
    print("====")
    print(render_template('complextest.txt', {'b': ['abc', 'def']}))
    print("====")
    print(render_template('safetest.txt', {'d': 'username'}))
    print("====")
    print(render_template('commenttest.txt', {'d': 'username'}))
    print("====")
