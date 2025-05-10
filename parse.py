def parse_file(fisier):
    formula = [[]]
    nr_variabile = nr_clauze = 0
    with open(fisier) as f:
        for linie in f:
            parti = linie.strip().split()
            if not parti or parti[0] == 'c':
                continue
            if parti[0] == 'p':
                nr_variabile = int(parti[2])
                nr_clauze = int(parti[3])
            else:
                for lit in parti:
                    valoare = int(lit)
                    if valoare == 0:
                        formula.append([])
                    else:
                        formula[-1].append(valoare)
    if not formula[-1]:
        formula.pop()
    return formula, nr_variabile, nr_clauze
