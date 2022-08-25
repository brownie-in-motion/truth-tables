class Proposition:
    def __init__(self, kind, children, data=None):
        self.kind = kind
        self.children = children
        self.values = set()
        self.data = data

        if kind == 'value':
            self.values.add(children[0])
        else:
            for child in children:
                self.values |= child.values

    @staticmethod
    def new(name):
        return Proposition('value', (name,))

    def evaluate(self, values):
        match self.kind:
            case 'value':
                return values[self.children[0]]
            case 'and':
                return (
                    self.children[0].evaluate(values) and
                    self.children[1].evaluate(values)
                )
            case 'or':
                return (
                    self.children[0].evaluate(values) or
                    self.children[1].evaluate(values)
                )
            case 'implies':
                return (
                    not self.children[0].evaluate(values) or
                    self.children[1].evaluate(values)
                )
            case 'implies_left':
                return (
                    self.children[0].evaluate(values) or
                    not self.children[1].evaluate(values)
                )
            case 'not':
                return not self.children[0].evaluate(values)
            case 'iff':
                return (
                    self.children[0].evaluate(values) and
                    self.children[1].evaluate(values)
                )

    def __and__(self, other):
        return Proposition('and', (self, other))

    def __or__(self, other):
        return Proposition('or', (self, other))

    def __gt__(self, other):
        return Proposition('implies', (self, other))

    def __lt__(self, other):
        return Proposition('implies_left', (self, other))

    def __invert__(self):
        return Proposition('not', (self,))

    def __eq__(self, other):
        return Proposition(
            'iff', (
                self > other,
                self < other,
            ),
            data=(self, other)
        )

    def __str__(self):
        match self.kind:
            case 'value':
                return self.children[0]
            case 'and':
                return f'({self.children[0]} and {self.children[1]})'
            case 'or':
                return f'({self.children[0]} or {self.children[1]})'
            case 'implies':
                return f'({self.children[0]} => {self.children[1]})'
            case 'implies_left':
                return f'({self.children[0]} <= {self.children[1]})'
            case 'not':
                return f'(not {self.children[0]})'
            case 'iff':
                assert self.data is not None
                return f'({self.data[0]} <=> {self.data[1]})'

    def tex_str(self):
        match self.kind:
            case 'value':
                return self.children[0]
            case 'and':
                return (
                    f'({self.children[0].tex_str()}'
                    ' \\land '
                    f'{self.children[1].tex_str()})'
                )
            case 'or':
                return (
                    f'({self.children[0].tex_str()}'
                    ' \\lor '
                    f'{self.children[1].tex_str()})'
                )
            case 'implies':
                return (
                    f'({self.children[0].tex_str()}'
                    ' \\Rightarrow '
                    f'{self.children[1].tex_str()})'
                )
            case 'implies_left':
                return (
                    f'({self.children[0].tex_str()}'
                    ' \\Leftarrow '
                    f'{self.children[1].tex_str()})'
                )
            case 'not':
                return (
                    f' \\lnot '
                    f'{self.children[0].tex_str()}'
                )
            case 'iff':
                assert self.data is not None
                return (
                    f'({self.data[0].tex_str()}'
                    ' \\Leftrightarrow '
                    f'{self.data[1].tex_str()})'
                )
        return ''


    def truth_table(self):
        # bfs through proposition tree to get all subtrees
        # this is extremely inefficient but i literally don't care

        propositions = []

        def dfs(root):
            if root.kind != 'value':
                for child in root.children:
                    dfs(child)
                propositions.append(root)

        dfs(self)

        # remove duplicates, but prefer them to be in front
        cleaned = []
        seen = set()
        for node in propositions:
            string = str(node)
            if string not in seen:
                cleaned.append(node)
                seen.add(string)

        # now this is also extremely inefficient because there is lots of
        # memoization that can happen. i again don't care.
        values = sorted(self.values)

        result = []
        for i in range(2 ** len(values)):
            result.append([])

            states = [not bool(int(x)) for x in f'{i:0{len(values)}b}']
            value_map = dict(zip(values, states))

            result[-1] = states + [node.evaluate(value_map) for node in cleaned]

        header = list(map(Proposition.new, values)) + cleaned

        return header, result

    # probably the worst thing i've ever written
    def tex_table(self):
        header, rows = self.truth_table()
        texed = [f'\\({x.tex_str()}\\)' for x in header]
        return (
            f'\\begin{{tabular}}{{{" ".join(["c"] * len(header))}}}\n'
            '\\toprule\n'
            f'{" & ".join(texed)} \\\\\n'
            '\\midrule\n'
        ) + ' \\\\\n'.join(
            ' & '.join(
                'T' if v else 'F' for v in row
            ) for row in rows
        ) + (
            ' \\\\\n\\bottomrule\n'
            '\\end{tabular}'
        )
