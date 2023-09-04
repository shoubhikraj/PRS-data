import autode as ade
from autode import CINEB

n_mid_images = 10

ade.Config.ORCA.keywords.grad = ["EnGrad", "PBEh-3c"]

ade.log.logger.setLevel("INFO")

rct = ade.Reactant("../orca-pbeh3c-opt-pdoac2-benzene-prod.xyz")
prod = ade.Product("../orca-pbeh3c-opt-pdoac2-benzene-rct.xyz")

cineb = CINEB.from_end_points(rct, prod, num=2+n_mid_images)

cineb.calculate(method=ade.methods.ORCA(), n_cores=4)

print("CINEB total number of iterations =", cineb.images[1].iteration)

if cineb.images.contains_peak:
    cineb.peak_species.print_xyz_file(filename=f"cineb-{n_mid_images}-peak.xyz")
else:
    print("No peak")
