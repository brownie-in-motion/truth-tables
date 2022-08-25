from propositions import Proposition

P = Proposition.new('P')
Q = Proposition.new('Q')
R = Proposition.new('R')

proposition_a = ((P > Q) & (Q > R)) > (P > R)
proposition_b = ((P | Q) & ~P) > Q
proposition_c = proposition_a & proposition_b

print(proposition_c.tex_table())
