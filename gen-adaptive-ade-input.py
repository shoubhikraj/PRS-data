import shutil
import pathlib
import pandas as pd


df = pd.read_csv("reactions_to_bench.csv", header=0)

begin_text = (
    "import autode as ade\n"
    "from autode.adaptive import get_ts_adaptive_path\n"
    "from autode.bond_rearrangement import BondRearrangement"
    "from autode.bonds import FormingBond, BreakingBond\n\n"
    "ade.log.logger.setLevel('INFO')\n"
    "ade.Config.ORCA.keywords.grad = ['EnGrad','PBEh-3c']\n"
    "ade.Config.ORCA.keywords.low_opt = ['Opt', 'PBEh-3c']\n"
    "ade.Config.ORCA.keywords.opt = ['Opt', 'PBEh-3c']\n\n"
)
# bond rearrangement must be set manually => atoms are already mapped
main_text = (
    "bond_rearr = BondRearrangement(\n"
    "   forming_bonds =,\n"
    "   breaking_bonds =,\n"
    ")\n"
    "for i, pair in enumerate(bond_rearr.bbonds):\n"
    "   bond_rearr.bbonds[i] = BreakingBond(pair, rct, prod)\n"
    "for i, pair in enumerate(bond_rearr.fbonds):\n"
    "   bond_rearr.fbonds[i] = FormingBond(pair, rct, prod)\n"
    "ts_guess = get_ts_adaptive_path (rct, prod, ade.methods.ORCA(), bond_rearr, 'adaptive_hl')\n"
    "if cineb.images.contains_peak:\n"
    "   cineb.peak_species.print_xyz_file(filename='cineb-5-peak.xyz')\n"
)

    
for i in range(0, 8):
    charge = int(df["charge"].iloc[i])
    mult = int(df["multiplicity"].iloc[i])
    # create folder
    pathlib.Path(f"./adaptive/reaction-{i}/").mkdir(parents=True, exist_ok=True)
    # copy xyz files
    shutil.copyfile(f"./final_aligned_orca_opt/reaction-{i}/reaction-{i}-rct-orca.xyz",
                    f"./adaptive/reaction-{i}/reaction-{i}-rct-orca.xyz")
    shutil.copyfile(f"./final_aligned_orca_opt/reaction-{i}/reaction-{i}-prod-orca.xyz",
                    f"./adaptive/reaction-{i}/reaction-{i}-prod-orca.xyz")
    # The reactant and product must be set manually depending to start from
    # the species with the higher number of bonds
    mid_txt = (
        f"rct =? ade.Reactant('reaction-{i}-rct-orca.xyz', charge={charge}, mult={mult})\n"
        f"prod =? ade.Product('reaction-{i}-prod-orca.xyz', charge={charge}, mult={mult})\n\n"
    )
    with open(f"adaptive/reaction-{i}/reaction-{i}-ci-neb-5.py", "w") as fh:
        fh.write(
            begin_text + mid_txt + main_text
        )


