import shutil
import pathlib
import pandas as pd


df = pd.read_csv("reactions_to_bench.csv", header=0)

begin_text = (
    "import autode as ade\n"
    "from autode import CINEB\n\n"
    "ade.log.logger.setLevel('INFO')\n"
    "ade.Config.ORCA.keywords.grad = ['EnGrad','PBEh-3c']\n\n"
)
main_text = (
    "\ncineb = CINEB.from_end_points(\n"
    "   rct,\n"
    "   prod,\n"
    "   num = 18,\n"
    ")\n\n"
    "cineb.calculate(ade.methods.ORCA(), n_cores=4)\n"
    "if cineb.images.contains_peak:\n"
    "   cineb.peak_species.print_xyz_file(filename='cineb-20-peak.xyz')\n"
    "print('Total number of CI-NEB iters =', cineb.images[1].iteration*20)\n"
)

with open("orca-ts-irc-template.inp") as fh:
    ts_template = fh.read()
    
for i in range(0, 8):
    charge = int(df["charge"].iloc[i])
    mult = int(df["multiplicity"].iloc[i])
    # create folder
    pathlib.Path(f"./ci_neb_20/reaction-{i}/").mkdir(parents=True, exist_ok=True)
    # copy xyz files
    shutil.copyfile(f"./final_aligned_orca_opt/reaction-{i}/reaction-{i}-rct-orca.xyz",
                    f"./ci_neb_20/reaction-{i}/reaction-{i}-rct-orca.xyz")
    shutil.copyfile(f"./final_aligned_orca_opt/reaction-{i}/reaction-{i}-prod-orca.xyz",
                    f"./ci_neb_20/reaction-{i}/reaction-{i}-prod-orca.xyz")
    # write input files
    mid_txt = (
        f"rct = ade.Reactant('reaction-{i}-rct-orca.xyz', charge={charge}, mult={mult})\n"
        f"prod = ade.Product('reaction-{i}-prod-orca.xyz', charge={charge}, mult={mult})\n"
    )
    with open(f"ci_neb_20/reaction-{i}/reaction-{i}-ci-neb-20.py", "w") as fh:
        fh.write(
            begin_text + mid_txt + main_text
        )
    
    pathlib.Path(f"./ci_neb_20/reaction-{i}/ts-opt/").mkdir(exist_ok=True)
    ts_inpfilebase = f"reaction-{i}-cineb20_optts"
    with open(f"./ci_neb_20/reaction-{i}/ts-opt/"+ts_inpfilebase+".inp", "w") as fh2:
        text = ts_template.replace("template.xyz", "../cineb-20-peak.xyz")
        text = text.replace("inpfile", ts_inpfilebase)
        fh2.write(text)
    

