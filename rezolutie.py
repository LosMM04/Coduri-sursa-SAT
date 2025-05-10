import parse
import datetime

def main():
    fisier = "test9.cnf"
    formula, _, _ = parse.parse_file(fisier)

    inceput = datetime.datetime.now()
    rezultat = rezolutie(formula)
    sfarsit = datetime.datetime.now()

    durata = (sfarsit - inceput).total_seconds() * 1000
    with open("rezultate_rezolutie.txt", "a") as f:
        if rezultat:
            f.write("NESATISFIABIL\n")
        else:
            f.write("SATISFIABIL\n")
        f.write(f"{durata:.2f} ms\n")
        f.write("\n")

def rezolva(cl1, cl2):
    for lit in cl1:
        if -lit in cl2:
            rez = set(cl1 + cl2)
            rez.discard(lit)
            rez.discard(-lit)
            return list(rez)
    return None

def rezolutie(formula):
    multime_initiala = [frozenset(cl) for cl in formula]
    cunoscute = set(multime_initiala)
    perechi_verificate = set()

    while True:
        perechi_noi = set()
        lista_ordonata = sorted(cunoscute, key=len)
        for i in range(len(lista_ordonata)):
            for j in range(i + 1, len(lista_ordonata)):
                cl1 = lista_ordonata[i]
                cl2 = lista_ordonata[j]
                if (cl1, cl2) in perechi_verificate or (cl2, cl1) in perechi_verificate:
                    continue
                perechi_verificate.add((cl1, cl2))
                rez = rezolva(list(cl1), list(cl2))
                if rez is not None:
                    rez_set = frozenset(rez)
                    if not rez_set:
                        return True
                    if rez_set not in cunoscute:
                        perechi_noi.add(rez_set)
        if not perechi_noi:
            return False
        cunoscute.update(perechi_noi)

if __name__ == '__main__':
    main()
