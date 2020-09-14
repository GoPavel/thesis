import argparse
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np

file_names = [
    'HahnAcyclic',
    'HahnDom',
    'HahnEquational',
    'HahnMaxElt',
    'HahnMinElt',
    'HahnPath',
    'HahnRelationsBasic'
]

raw = defaultdict(list)


def analyze():
    prev, ans = '', True
    proof_stat = defaultdict(int)
    for name in file_names:
        for ls in raw[name]:
            proof_stat['total'] += 1
            p = ''.join(ls)
            if 'kat' in p:
                proof_stat['changed'] += 1
                print(p)
                if prev == p:
                    is_full = ans
                else:
                    is_full = bool(input('full? '))
                    prev = p
                    ans = is_full
                if is_full:
                    proof_stat['full'] += 1
                    if 'kat' in p and 'hkat' not in p:
                        proof_stat['full_proof_with_kat'] += 1
                    if 'hkat' in p:
                        proof_stat['full_proof_with_hkat'] += 1
                    if 'hkat' in p and "hkat''" not in p:
                        proof_stat['full_proof_with_hkat_light'] += 1
                    if "hkat''" in p:
                        proof_stat['full_proof_with_hkat_hard'] += 1
                else:
                    if 'kat' in p and 'hkat' not in p:
                        proof_stat['part_proof_with_kat'] += 1
                    if 'hkat' in p:
                        proof_stat['part_proof_with_hkat'] += 1
                    if 'hkat' in p and "hkat''" not in p:
                        proof_stat['part_proof_with_hkat_light'] += 1
                    if "hkat''" in p:
                        proof_stat['part_proof_with_hkat_hard'] += 1
                    proof_stat['partial'] += 1
            proof_stat['line_total'] += len(ls)

    for k, v in proof_stat.items():
        print(f'>>> {k}: {v}')

    sizes = [proof_stat['total'] - (proof_stat['changed']), proof_stat['full'], proof_stat['partial']]
    print(f'proofs: {sizes}')
    # labels = f'Не именилось: {sizes[0]}', f'Упростилось: {sizes[1]}'
    explode = (0, 0.1, 0.1)

    plt.rcParams.update({'font.size': 28})
    plt.rcParams['figure.figsize'] = 16, 9

    fig, (ax1, ax2) = plt.subplots(1, 2)

    def func(pct, sizes):
        absolute = int(pct / 100. * sum(sizes))
        return "{:.1f}%\n({:d})".format(pct, absolute)

    ax1.pie(sizes, explode=explode, autopct=lambda pct: func(pct, sizes), startangle=90)
    ax1.set_title("Количество доказательств")
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.legend(['Не изменилось', 'Полностью автоматизировано', 'Частично автоматизировано'])

    sizes = [2178, 320, 151]
    print(f'lines: {sizes}')
    # labels = (f'Не изменилось: {sizes[0]}', f'Упростилось: {sizes[1]}')
    ax2.pie(sizes, explode=(0, 0.1, 0.1), autopct=lambda pct: func(pct, sizes), startangle=90)
    ax2.set_title('Количество строк')
    ax2.axis('equal')
    plt.savefig('stat.png')


def main(args):
    assert 'temp' in args.path_dir
    for name in file_names:
        with open(f'{args.path_dir}/{name}.v') as f:
            proof = []
            for l in f:
                if "Proof." in l or proof:
                    proof.append(l)
                if "Qed." in l:
                    raw[name].append(proof)
                    proof = []

    analyze()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path_dir", type=str)

    main(parser.parse_args())
