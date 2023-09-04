import shutil
import pathlib
import pandas as pd


df = pd.read_csv("reactions_to_bench.csv", header=0)

begin_text = (
    "import autode as ade\n"
    "from autode.bracket import DHSGS\n\n"
    "ade.log.logger.setLevel('INFO')\n"
    "ade.Config.ORCA.keywords.grad = ['EnGrad','PBEh-3c']\n\n"
)
main_text = (
    "\ndhsgs = DHSGS(\n"
    "   initial_species = rct,\n"
    "   final_species = prod,\n"
    "   maxiter = 1000,\n"
    "   step_size = 0.2,\n"
    "   gtol = 1e-3,\n"
    "   dist_tol = 0.5,\n"
    ")\n\n"
    "dhsgs.calculate(ade.methods.ORCA(), n_cores=4)\n"
    "print('Total number of DHS-GS iters =', dhsgs._micro_iter)\n"
)


for i in range(0, 8):
    charge = int(df["charge"].iloc[i])
    mult = int(df["multiplicity"].iloc[i])
    # create folder
    pathlib.Path(f"./dhs_gs/reaction-{i}/").mkdir(parents=True, exist_ok=True)
    # copy xyz files
    shutil.copyfile(f"./final_aligned_orca_opt/reaction-{i}/reaction-{i}-rct-orca.xyz",
                    f"./dhs_gs/reaction-{i}/reaction-{i}-rct-orca.xyz")
    shutil.copyfile(f"./final_aligned_orca_opt/reaction-{i}/reaction-{i}-prod-orca.xyz",
                    f"./dhs_gs/reaction-{i}/reaction-{i}-prod-orca.xyz")
    # write input files
    mid_txt = (
        f"rct = ade.Reactant('reaction-{i}-rct-orca.xyz', charge={charge}, mult={mult})\n"
        f"prod = ade.Product('reaction-{i}-prod-orca.xyz', charge={charge}, mult={mult})\n"
    )
    with open(f"dhs_gs/reaction-{i}/reaction-{i}-dhs-gs.py", "w") as fh:
        fh.write(
            begin_text + mid_txt + main_text
        )


