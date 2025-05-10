import parse
import datetime

def main():
    fisier = "test1.cnf"
    formula, _, _ = parse.parse_file(fisier)

    inceput = datetime.datetime.now()
    rezultat = rezolutie_dp(formula)
    sfarsit = datetime.datetime.now()

    durata = (sfarsit - inceput).total_seconds() * 1000
    with open("rezultate_dp.txt", "a") as f:
        if rezultat:
            f.write("NESATISFIABIL\n")
        else:
            f.write("SATISFIABIL\n")
        f.write(f"{durata:.2f} ms\n")
        f.write("\n")  # Linie goală pentru separarea testelor

def rezolva(cl1, cl2, variabila):
    if variabila in cl1 and -variabila in cl2:
        rez = (cl1 | cl2) - {variabila, -variabila}
        return frozenset(rez)
    elif -variabila in cl1 and variabila in cl2:
        rez = (cl1 | cl2) - {variabila, -variabila}
        return frozenset(rez)
    return None

def rezolutie_dp(formula):
    cunoscute = set(frozenset(cl) for cl in formula)

    while True:
        schimbat = False
        unitati = {next(iter(cl)) for cl in cunoscute if len(cl) == 1}
        while unitati:
            lit = unitati.pop()
            noua_cunoscute = set()
            for cl in cunoscute:
                if lit in cl:
                    continue
                if -lit in cl:
                    new_clause = cl - {-lit}
                    if not new_clause:
                        return True
                    noua_cunoscute.add(frozenset(new_clause))
                else:
                    noua_cunoscute.add(cl)
            cunoscute = noua_cunoscute
            schimbat = True
        toti_literalii = [lit for cl in cunoscute for lit in cl]
        aparitii = set(toti_literalii)
        puri = {lit for lit in aparitii if -lit not in aparitii}
        if puri:
            cunoscute = {cl for cl in cunoscute if not any(lit in cl for lit in puri)}
            schimbat = True

        if schimbat:
            continue
        if not cunoscute:
            return False
        if any(len(cl) == 0 for cl in cunoscute):
            return True

        toti_literalii = set(lit for cl in cunoscute for lit in cl)
        variabile = sorted({abs(lit) for lit in toti_literalii})
        if not variabile:
            return False

        var = variabile[0]

        pozitive = [cl for cl in cunoscute if var in cl]
        negative = [cl for cl in cunoscute if -var in cl]

        rezolvente = set()
        for cl1 in pozitive:
            for cl2 in negative:
                rez = rezolva(cl1, cl2, var)
                if rez is not None:
                    if not rez:
                        return True
                    rezolvente.add(rez)

        cunoscute = {cl for cl in cunoscute if var not in cl and -var not in cl}
        cunoscute.update(rezolvente)

if __name__ == '__main__':
    main()
