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
        x_ranges = [[0.00, 6.00, 0.100]]
        y_ranges = [[0.00, 6.00, 0.100]]

    for x_range, y_range in zip(x_ranges, y_ranges):
        print('\033[F', end='')
        print("Gerando nova malha...              ")
        print(ctext(f"Passos: ({x_range[-1]}, {y_range[-1]})", 'm'))

        tunnel = Tunnel(x_range, y_range, params)

        print(f"\n{ctext('Meshgrids inicializadas!', 'g')}")

        if item == 'a':
            tunnel.plot_meshgrid('C')
            continue

        while True:
            print(f"{ctext('C.', 'c')} Corrente de escoamento")
            print(f"{ctext('u.', 'c')} Componente horizontal da velocidade")
            print(f"{ctext('v.', 'c')} Componente vertical da velocidade")
            print(f"{ctext('T.', 'c')} Temperatura")

            choosen_meshgrid = validate_input(
                f"Entre com {ctext('C', 'c')}, {ctext('u', 'c')}, {ctext('v', 'c')}, {ctext('T', 'c')} ou pressione {ctext('ENTER', 'g')} para continuar: ",
                ['c', 'u', 'v', 't', 'ENTER'],
                'ENTER'
            )

            if choosen_meshgrid in ['c', 't']: choosen_meshgrid = choosen_meshgrid.upper()
            elif choosen_meshgrid in ['u', 'v']: pass
            else: break

            tunnel.plot_meshgrid(choosen_meshgrid)

        print('\nCalculando e plotando a corrente de escoamento...')
        tunnel.apply_liebmann_for('C', 1.85, 0.01)
        tunnel.plot('C')

    if item == 'a': return

    input(f"\nPressione {ctext('ENTER', 'g')} para continuar")

    print('\033[F', end='')
    print('Calculando e plotando a velocidade...')
    tunnel.calculate('V')
    tunnel.plot('V')

    input(f"\nPressione {ctext('ENTER', 'g')} para continuar")

    print('\033[F', end='')
    print('Calculando e plotando a pressão no domínio e no carro...')
    tunnel.calculate('p')
    tunnel.plot('p')
    tunnel.plot('pcar')

    input(f"\nPressione {ctext('ENTER', 'g')} para continuar")

    tunnel.calculate('F')
    print('\033[F', end='')
    print(f"{ctext('Força de Levantamento na Carroceria:', 'b')} {tunnel.F:.2f} N")

    input(f"\nPressione {ctext('ENTER', 'g')} para continuar")

    print('\nCalculando e plotando a temperatura...')
    tunnel.apply_liebmann_for('T', 1.85, 0.01)
    tunnel.plot('T')

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
