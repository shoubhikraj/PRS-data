import autode as ade
import numpy as np
from autode.utils import work_in
import pickle

ade.Config.n_cores = 8
ade.log.logger.setLevel("INFO")
ade.Config.ORCA.keywords.grad = ["EnGrad", "PBEh-3c"]
ade.Config.ORCA.keywords.opt = ["Opt", "PBEh-3c"]
ade.Config.ORCA.keywords.low_opt = ['Opt', 'PBEh-3c']

# reload pes
with open("R4-2D-fullsave.pkl", "rb") as fh:
    pes = pickle.load(fh)
    
tmp_mol = ade.Molecule("manual/reaction4-IEIP_ts_guess_scan_5-4_orca.xyz", charge=1, mult=1)
assert np.isnan(pes[5,4])
pes._coordinates[5,4] = np.array(tmp_mol.coordinates)
pes._energies[5,4] = -1288.399538019789


pes.plot("R4-2D.png")
pes.plot("R4-2D-smooth.png", interp_factor=2)

for idx, ts in enumerate(pes.ts_guesses()):
    ts.print_xyz_file(filename=f"ts_guess_{idx}.xyz")
