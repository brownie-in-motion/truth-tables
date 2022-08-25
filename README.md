# Truth Tables

A hacky Python DSL for generating truth tables with intermediate steps. Mostly
useful for introductory CS classes. Only outputs tex, which requires the
`booktabs` package to be rendered.

Want ascii tables? PRs welcome. I don't need this anymore.

## Usage

Here is an example of basic usage:

```python
from propositions import Proposition

P = Proposition.new('P')
Q = Proposition.new('Q')

proposition = ((P | Q) & ~P) > Q

print(proposition.tex_table())
```

This produces

```
\begin{tabular}{c c c c c c}
\toprule
\(P\) & \(Q\) & \((P \lor Q)\) & \( \lnot P\) & \(((P \lor Q) \land  \lnot P)\) & \((((P \lor Q) \land  \lnot P) \Rightarrow Q)\) \\
\midrule
T & T & T & F & F & T \\
T & F & T & F & F & T \\
F & T & T & T & T & T \\
F & F & F & T & F & T \\
\bottomrule
\end{tabular}
```

which renders to

![rendered example](https://brown.ee/Q191GNMJ.png)
