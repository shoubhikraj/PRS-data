import autode as ade
from autode.utils import work_in
import pickle

ade.Config.n_cores = 8
ade.log.logger.setLevel("INFO")
ade.Config.ORCA.keywords.grad = ["EnGrad", "PBEh-3c"]
ade.Config.ORCA.keywords.opt = ["Opt", "PBEh-3c"]
ade.Config.ORCA.keywords.low_opt = ['Opt', 'PBEh-3c']

pes = ade.pes.RelaxedPESnD(
    species = ade.Molecule("reaction4-IEIP_ts_guess.xyz", charge=1, mult=1),
    rs = {(0, 20): (2.6, 2.0, 15), (24, 30): (1.5, 1.3, 15)},
)

@work_in("scan")
def calc():
    pes.calculate(method=ade.methods.ORCA())

calc()
pes.save("R4-2Dscan.npz")
pes.plot("R4-2D.png")
pes.plot("R4-2D-smooth.png", interp_factor=2)

for idx, ts in enumerate(pes.ts_guesses()):
    ts.print_xyz_file(filename=f"ts_guess_{idx}.xyz")

with open("R4-2D-fullsave.pkl", "wb") as fh:
    pickle.dump(pes, fh, protocol=pickle.HIGHEST_PROTOCOL)
