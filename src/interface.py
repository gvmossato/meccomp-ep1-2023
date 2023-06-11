# ================================== #
# Intermédio entre scripts e usuário #
# ================================== #

import src.part1.solver as part1
import src.part2.solver as part2

from src.utils import validate_input, ctext


def start():
    while True:
        print("\nEscolha qual parte deseja resolver:")
        print(f"{ctext('1.', 'b')} Parte 1 — RK")
        print(f"{ctext('2.', 'b')} Parte 2 — MDF")

        choosen_part = validate_input(
            f"Entre com {ctext('1', 'b')}, {ctext('2', 'b')} ou {ctext('SAIR', 'r')} para finalizar: ",
            ['1', '2', 'sair']
        )

        if choosen_part == '1':
            print("\nEscolha item deseja resolver:")
            print(f"{ctext('A.', 'm')} Solução da equação diferencial")
            print(f"{ctext('B.', 'm')} Estudo da influência das constantes")

            choosen_item = validate_input(
                f"Entre com {ctext('A', 'm')} ou {ctext('B', 'm')}: ",
                ['a', 'b']
            )
            part1.solve(choosen_item)

        elif choosen_part == '2':
            print("\nEscolha qual item deseja resolver:")
            print(f"{ctext('A.', 'm')} Testes de discretização")
            print(f"{ctext('B.', 'm')} Solução completa com discretização adequada")
            print(f"{ctext('C.', 'm')} Estudo da variação da força de sustentação\n")

            choosen_item = validate_input(
                f"Entre com {ctext('A', 'm')}, {ctext('B', 'm')} ou {ctext('C', 'm')}: ",
                ['a', 'b', 'c']
            )
            part2.solve(choosen_item)

        else:
            break
