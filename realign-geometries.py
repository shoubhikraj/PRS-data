import pathlib
import numpy as np
import autode as ade
from autode.geom import get_rot_mat_kabsch
import pandas as pd


def align_species(first_species, second_species):
    assert first_species.n_atoms == second_species.n_atoms
    p_mat = first_species.coordinates.copy()
    p_mat -= np.average(p_mat, axis=0)
    first_species.coordinates = p_mat
    
    q_mat = second_species.coordinates.copy()
    q_mat -= np.average(q_mat, axis=0)
    second_species.coordinates = q_mat
    
    rot_mat = get_rot_mat_kabsch(p_mat, q_mat)
    rotated_p_mat = np.dot(rot_mat, p_mat.T).T
    first_species.coordinates = rotated_p_mat
    return None
   
df = pd.read_csv("reactions_to_bench.csv", header=0)
    
for i in range(7, 8):
    charge = df["charge"].iloc[i]
    rct = ade.Molecule(f"orca_minima_opt/reaction-{i}/reaction-{i}-rct-pbeh3c-orca_opt.xyz", charge=charge)
    prod = ade.Molecule(f"orca_minima_opt/reaction-{i}/reaction-{i}-prod-pbeh3c-orca_opt.xyz", charge=charge)
    align_species(rct, prod)
    pathlib.Path(f"./final_aligned_orca_opt/reaction-{i}/").mkdir(parents=True, exist_ok=True)
    rct.print_xyz_file(filename=f"final_aligned_orca_opt/reaction-{i}/reaction-{i}-rct-orca.xyz")
    prod.print_xyz_file(filename=f"final_aligned_orca_opt/reaction-{i}/reaction-{i}-prod-orca.xyz")
    


