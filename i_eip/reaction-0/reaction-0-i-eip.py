import autode as ade
from autode.bracket.eip import IEIP

ade.log.logger.setLevel('INFO')
ade.Config.ORCA.keywords.grad = ['EnGrad','PBEh-3c']
ade.Config.ORCA.keywords.low_sp = ['SP', 'PBEh-3c']

rct = ade.Reactant('reaction-0-rct-orca.xyz', charge=0, mult=1)
prod = ade.Product('reaction-0-prod-orca.xyz', charge=0, mult=1)

ieip = IEIP(
   initial_species = rct,
   final_species = prod,
   maxiter = 1000,
)

ieip.calculate(ade.methods.ORCA(), n_cores=4)
print('Total number of i-EIP gradient iters =', ieip._macro_iter + 4)
