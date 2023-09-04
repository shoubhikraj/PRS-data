import autode as ade
from autode import CINEB

ade.log.logger.setLevel('INFO')
ade.Config.ORCA.keywords.grad = ['EnGrad','PBEh-3c']

rct = ade.Reactant('reaction-4-rct-orca.xyz', charge=1, mult=1)
prod = ade.Product('reaction-4-prod-orca.xyz', charge=1, mult=1)

cineb = CINEB.from_end_points(
   rct,
   prod,
   num = 18,
)

cineb.calculate(ade.methods.ORCA(), n_cores=4)
if cineb.images.contains_peak:
   cineb.peak_species.print_xyz_file(filename='cineb-20-peak.xyz')
print('Total number of CI-NEB iters =', cineb.images[1].iteration*20)
