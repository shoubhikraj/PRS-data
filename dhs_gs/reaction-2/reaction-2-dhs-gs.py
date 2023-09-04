import autode as ade
from autode.bracket import DHSGS

ade.log.logger.setLevel('INFO')
ade.Config.ORCA.keywords.grad = ['EnGrad','PBEh-3c']

rct = ade.Reactant('reaction-2-rct-orca.xyz', charge=-1, mult=1)
prod = ade.Product('reaction-2-prod-orca.xyz', charge=-1, mult=1)

dhsgs = DHSGS(
   initial_species = rct,
   final_species = prod,
   maxiter = 1000,
   step_size = 0.2,
   gtol = 1e-3,
   dist_tol = 0.5,
)

dhsgs.calculate(ade.methods.ORCA(), n_cores=4)
print('Total number of DHS-GS iters =', dhsgs._micro_iter)
