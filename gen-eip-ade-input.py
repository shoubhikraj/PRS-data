import shutil
import pathlib
import pandas as pd


df = pd.read_csv("reactions_to_bench.csv", header=0)

begin_text = (
    "import autode as ade\n"
    "from autode.bracket.eip import IEIP\n\n"
    "ade.log.logger.setLevel('INFO')\n"
    "ade.Config.ORCA.keywords.grad = ['EnGrad','PBEh-3c']\n"
    "ade.Config.ORCA.keywords.low_sp = ['SP', 'PBEh-3c']\n\n"
)

main_text = (
    "\nieip = IEIP(\n"
    "   initial_species = rct,\n"
    "   final_species = prod,\n"
    "   maxiter = 1000,\n"
    ")\n\n"
    "ieip.calculate(ade.methods.ORCA(), n_cores=4)\n"
    "print('Total number of i-EIP gradient iters =', ieip._macro_iter + 4)\n"
)


for i in range(0, 8):
    charge = int(df["charge"].iloc[i])
    mult = int(df["multiplicity"].iloc[i])
    # create folder
    pathlib.Path(f"./i_eip/reaction-{i}/").mkdir(parents=True, exist_ok=True)
    # copy xyz files
    shutil.copyfile(f"./final_aligned_orca_opt/reaction-{i}/reaction-{i}-rct-orca.xyz",
                    f"./i_eip/reaction-{i}/reaction-{i}-rct-orca.xyz")
    shutil.copyfile(f"./final_aligned_orca_opt/reaction-{i}/reaction-{i}-prod-orca.xyz",
                    f"./i_eip/reaction-{i}/reaction-{i}-prod-orca.xyz")
    # write input files
    mid_txt = (
        f"rct = ade.Reactant('reaction-{i}-rct-orca.xyz', charge={charge}, mult={mult})\n"
        f"prod = ade.Product('reaction-{i}-prod-orca.xyz', charge={charge}, mult={mult})\n"
    )
    with open(f"i_eip/reaction-{i}/reaction-{i}-i-eip.py", "w") as fh:
        fh.write(
            begin_text + mid_txt + main_text
        )


