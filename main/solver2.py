# ============================== #
# Script para solução da Parte 2 #
# ============================== #

from main.src.utils import ctext, validate_input
from main.src.params import params
from main.src.lib2 import Tunnel


def solve(item):
    if item == 'a':
        x_ranges = [
            [0.00, 6.00, 0.500],
            [0.00, 6.00, 0.050],
            [0.00, 6.00, 0.025],
        ]
        y_ranges = [
            [0.00, 6.00, 0.500],
            [0.00, 6.00, 0.050],
            [0.00, 6.00, 0.025],
        ]
    else:
        x_ranges = [[0.00, 6.00, 0.050]]
        y_ranges = [[0.00, 6.00, 0.050]]

    for x_range, y_range in zip(x_ranges, y_ranges):
        print('\033[F', end='')
        print("Gerando nova malha...              ")
        print(ctext(f"Passos: ({x_range[-1]}, {y_range[-1]})", 'm'))

        tunnel = Tunnel(x_range, y_range, params)

        print(f"\n{ctext('Meshgrids inicializadas!', 'g')}")

        if item == 'a':
            tunnel.plot_meshgrid('V')
            continue

        while True:
            print(f"{ctext('V.', 'c')} Contornos para velocidade")

            choosen_meshgrid = validate_input(
                f"Entre com {ctext('V', 'c')} ou pressione {ctext('ENTER', 'g')} para continuar: ",
                ['v', 'ENTER'],
                'ENTER'
            )
            if choosen_meshgrid in ['v']: choosen_meshgrid = choosen_meshgrid.upper()
            else: break
            tunnel.plot_meshgrid(choosen_meshgrid)

        print('\nCalculando e plotando a distribuição de velocidades:')
        tunnel.apply_liebmann_for('V', 1.85, 0.01)
        tunnel.plot('V')

    if item == 'a': return

    # input(f"\nPressione {ctext('ENTER', 'g')} para continuar")

    # print('\033[F', end='')
    # print('Calculando e plotando a densidade de corrente...')
    # plate.calculate_flux('J')
    # plate.plot('J')

    # input(f"\nPressione {ctext('ENTER', 'g')} para continuar")

    # plate.calculate('i')
    # plate.calculate('R')
    # print('\033[F', end='')
    # print('Propriedades do bloco encontradas:')
    # print(f"{ctext('Corrente através da parede:', 'b')} {plate.i*1000:.4} mA")
    # print(f"{ctext('Resistência:', 'b')} {plate.R/1000:.4} kΩ")

    # input(f"\nPressione {ctext('ENTER', 'g')} para continuar")

    # print('\033[F', end='')
    # print('Calculando e plotando a fonte de calor distribuído...')
    # plate.calculate('dot_q')
    # plate.plot('dot_q')

    # input(f"\nPressione {ctext('ENTER', 'g')} para continuar\r")

    # print('\033[F', end='')
    # print('Calculando e plotando a distribuição de temperatura...')
    # plate.apply_liebmann_for('T', 1.75, 0.0001)
    # plate.plot('T')

    # input(f"\nPressione {ctext('ENTER', 'g')} para continuar\r")

    # print('\033[F', end='')
    # print('Calculando e plotando o fluxo de calor...')
    # plate.calculate_flux('Q')
    # plate.plot('Q')

    # input(f"\nPressione {ctext('ENTER', 'g')} para continuar\r")

    # print('\033[F', end='')
    # plate.calculate('q_conv')
    # print('Propriedade encontrada:')
    # print(f"{ctext('Perda de calor por convecção:', 'b')} {plate.q_conv*1000:.4} mW/m²")
    return
