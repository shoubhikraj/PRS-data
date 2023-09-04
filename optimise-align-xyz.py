import pathlib
import numpy as np
import autode as ade
from autode.geom import get_rot_mat_kabsch
from autode.utils import work_in_tmp_dir
import pandas as pd

ade.log.logger.setLevel("INFO")

@work_in_tmp_dir()
def optimise_mol(mol):
    mol.optimise(method=ade.methods.XTB())
    return None
    
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
    
for i in range(0, 8):
    charge = df["charge"].iloc[i]
    rct = ade.Molecule(f"drawn_xyz_files/reaction-{i}/reaction-{i}-drawn-rct.xyz", charge=charge)
    prod = ade.Molecule(f"drawn_xyz_files/reaction-{i}/reaction-{i}-drawn-prod.xyz", charge=charge)
    optimise_mol(rct)
    optimise_mol(prod)
    align_species(rct, prod)
    pathlib.Path(f"./optimised_aligned_xyz_files/reaction-{i}/").mkdir(parents=True, exist_ok=True)
    rct.print_xyz_file(filename=f"optimised_aligned_xyz_files/reaction-{i}/reaction-{i}-rct-xtb.xyz")
    prod.print_xyz_file(filename=f"optimised_aligned_xyz_files/reaction-{i}/reaction-{i}-prod-xtb.xyz")
    


