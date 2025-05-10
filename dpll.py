import datetime
import parse

def main():
    fisier = "Pigeon_Hole_2.cnf"
    formula, _, _ = parse.parse_file(fisier)

    inceput = datetime.datetime.now()
    rezultat = dpll(formula)
    sfarsit = datetime.datetime.now()

    durata = (sfarsit - inceput).total_seconds() * 1000


    with open("rezultate_dpll.txt", "a") as f:
        if rezultat:
            f.write("SATISFIABIL\n")
        else:
            f.write("NESATISFIABIL\n")
        f.write(f"{durata:.2f} ms\n")
        f.write("\n")


def dpll(formula, asignari=None):
    if asignari is None:
        asignari = {}
    formula = [cl for cl in formula if cl]
    if not formula:
        return True
    if any(len(cl) == 0 for cl in formula):
        return False
    unitari = [cl[0] for cl in formula if len(cl) == 1]
    while unitari:
        lit = unitari.pop()
        asignari[abs(lit)] = lit > 0
        formula = simplifica(formula, lit)
        if formula is None:
            return False
        if not formula:
            return True
        unitari = [cl[0] for cl in formula if len(cl) == 1]
    toate_literalii = [lit for cl in formula for lit in cl]
    aparitii = set(toate_literalii)
    puri = {lit for lit in aparitii if -lit not in aparitii}
    for lit in puri:
        asignari[abs(lit)] = lit > 0
        formula = simplifica(formula, lit)
        if formula is None:
            return False
        if not formula:
            return True
    frecvente = {}
    for cl in formula:
        for lit in cl:
            if abs(lit) not in asignari:
                if lit in frecvente:
                    frecvente[lit] += 1
                else:
                    frecvente[lit] = 1

    if not frecvente:
        return True

    lit_ales = max(frecvente, key=lambda x: frecvente[x])
    var = abs(lit_ales)
    asignari_cp = asignari.copy()
    asignari_cp[var] = lit_ales > 0
    if dpll(simplifica(formula, lit_ales), asignari_cp):
        return True
    asignari_cp = asignari.copy()
    asignari_cp[var] = lit_ales < 0
    if dpll(simplifica(formula, -lit_ales), asignari_cp):
        return True

    return False

def simplifica(formula, literal):
    noua_formula = []
    for cl in formula:
        if literal in cl:
            continue
        if -literal in cl:
            cl_noua = [l for l in cl if l != -literal]
            if not cl_noua:
                return None
            noua_formula.append(cl_noua)
        else:
            noua_formula.append(cl)
    return noua_formula

if __name__ == '__main__':
    main()
