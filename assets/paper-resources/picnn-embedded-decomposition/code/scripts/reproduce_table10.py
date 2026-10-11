"""Rebuild the SI table from original per-path CSVs; no test-based retuning."""
from pathlib import Path
import csv, json, sys
import numpy as np
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT))


def mean(path):
    with path.open(encoding='utf-8',newline='') as f:
        return float(np.mean([float(row['NPC']) for row in csv.DictReader(f)]))


def main():
    references = json.loads((ROOT/'reference_results/supplementary_table10.json').read_text(encoding='utf-8'))
    print('Stages,Uncertainty,8-node SDDP,27-node SDDP,2-period RH,Proposed')
    for row in references:
        t,std = row['stages'],round(100*row['uncertainty'])
        folder = ROOT/f'reference_results/T{t}_std{std}'
        values = []
        for nodes in [8,27]:
            value = np.mean([mean(folder/f'SDDP{nodes}_seed{seed}.csv') for seed in [17,23,29]])
            if abs(value-row[f'SDDP{nodes}'])>1e-10:
                raise RuntimeError('Stored table and source path means differ')
            values.append(value)
        if not row['approximate']:
            training_seed = {(6,10):0,(6,30):4,(24,30):1}[(t,std)]
            path = folder/f'T{t}_std{std}_PICNN{row["successors"]}_seed{training_seed}.csv'
            if abs(mean(path)-row['Proposed'])>1e-10:
                raise RuntimeError('Stored Proposed cost and policy path means differ')
        approximate = '≈' if row['approximate'] else ''
        print(f'{t},{std}%,{values[0]:.3f},{values[1]:.3f},{row["RH2"]:.3f},{approximate}{row["Proposed"]:.3f}')


if __name__=='__main__':
    main()
