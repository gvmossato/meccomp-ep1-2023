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
            [0.00, 6.00, 0.100],
            [0.00, 6.00, 0.050],
        ]
        y_ranges = [
            [0.00, 6.00, 0.500],
            [0.00, 6.00, 0.100],
            [0.00, 6.00, 0.050],
        ]
    else:
        x_ranges = [[0.00, 6.00, 0.1]]
        y_ranges = [[0.00, 6.00, 0.1]]

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
            print(f"{ctext('w.', 'c')} Componente horizontal do fluxo de calor")
            print(f"{ctext('z.', 'c')} Componente vertical do fluxo de calor")

            choosen_meshgrid = validate_input(
                f"Entre com {ctext('C', 'c')}, {ctext('u', 'c')}, {ctext('v', 'c')}, {ctext('T', 'c')}, {ctext('w', 'c')}, {ctext('z', 'c')} ou pressione {ctext('ENTER', 'g')} para continuar: ",
                ['c', 'u', 'v', 't', 'w', 'z', 'ENTER'],
                'ENTER'
            )

            if choosen_meshgrid in ['c', 't']: choosen_meshgrid = choosen_meshgrid.upper()
            elif choosen_meshgrid in ['u', 'v', 'w', 'z']: pass
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
    tunnel.apply_liebmann_for('T', 1.05, 0.0001)
    tunnel.plot('Tsurf')
    tunnel.plot('Tmap')

    input(f"\nPressione {ctext('ENTER', 'g')} para continuar")

    print('Calculando e plotando o fluxo de calor no domínio e no carro...')
    tunnel.calculate('q')
    tunnel.calculate('qcar')
    tunnel.plot('q')
    print(f"{ctext('Fluxo de calor através da carroceria:', 'b')} {tunnel.Q:.2f} W")

    input(f"\nPressione {ctext('ENTER', 'g')} para continuar")

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
