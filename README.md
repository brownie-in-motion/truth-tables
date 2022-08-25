# Truth Tables

![example image](https://brown.ee/Q191GNMJ.png)

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

proposition = ((P | Q) & ~P) > (Q == P)

print(proposition.tex_table())
```

This produces

```
\begin{tabular}{c c c c c c c c c}
\toprule
\(P\) & \(Q\) & \((P \lor Q)\) & \( \lnot P\) & \(((P \lor Q) \land  \lnot P)\) & \((Q \Rightarrow P)\) & \((Q \Leftarrow P)\) & \((Q \Leftrightarrow P)\) & \((((P \lor Q) \land  \lnot P) \Rightarrow (Q \Leftrightarrow P))\) \\
\midrule
T & T & T & F & F & T & T & T & T \\
T & F & T & F & F & T & F & F & T \\
F & T & T & T & T & F & T & F & F \\
F & F & F & T & F & T & T & T & T \\
\bottomrule
\end{tabular}
```

which renders to the following image:

![rendered image](https://brown.ee/t9vAHaul.png)

You might notice that the bidirectional implication has two intermediate steps,
one for each direction. This is because the class I took had extremely deranged
requirements.
