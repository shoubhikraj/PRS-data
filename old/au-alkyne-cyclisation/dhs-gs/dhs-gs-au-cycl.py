import autode as ade
from autode.bracket.dhs import DHSGS

ade.log.logger.setLevel("INFO")
ade.Config.n_cores = 6

ade.Config.ORCA.keywords.grad = ["EnGrad", "PBEh-3c"]
ade.Config.ORCA.keywords.sp = ["SP", "PBEh-3c"]

ade.log.logger.setLevel("INFO")

rct = ade.Reactant("../orca-pbeh3c-opt-pdoac2-au-cycl-rct.xyz")
prod = ade.Product("../orca-pbeh3c-opt-pdoac2-au-cycl-prod.xyz")

dhs = DHSGS(
    initial_species=rct,
    final_species=prod,
    maxiter=1000,
    step_size=0.15,
    dist_tol = 1.0,
)

dhs.calculate(method=ade.methods.ORCA(), n_cores=6)
dhs.plot_energies()
dhs.run_cineb()
dhs.write_trajectories()
print("Total number of ORCA iterations = ", dhs._micro_iter)
dhs.ts_guess.print_xyz_file(filename="peak-au-cycl-dhsgs.xyz")
