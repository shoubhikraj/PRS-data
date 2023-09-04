import autode as ade

ade.Config.n_cores = 8

ade.Config.ORCA.keywords.grad = ["EnGrad", "PBEh-3c"]
ade.Config.ORCA.keywords.hess = ["Freq", "PBEh-3c"]
ade.Config.ORCA.keywords.opt_ts.functional = "PBEh-3c"
ade.Config.ORCA.keywords.opt_ts.basis_set = None
ade.Config.ORCA.keywords.opt_ts.dispersion = None

ade.log.logger.setLevel("INFO")

rct1 = ade.Reactant("../orca-pbeh3c-opt-benzene-split.xyz")
rct2 = ade.Reactant("../orca-pbeh3c-opt-pdoac2-split.xyz")
prod = ade.Product("../orca-pbeh3c-opt-pdoac2-benzene-prod.xyz")

rxn = ade.Reaction(rct1, rct2, prod, name="pd-benzene")
rxn.locate_transition_state()

if rxn.ts is not None:
    rxn.ts.print_xyz_file(filename='guessed_ts.xyz')
