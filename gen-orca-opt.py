import shutil
import pathlib
import pandas as pd


df = pd.read_csv("reactions_to_bench.csv", header=0)

with open("orca-opt-template.inp") as fh:
    template = fh.read()
    
for i in range(0, 8):
    charge = df["charge"].iloc[i]
    mult = df["multiplicity"].iloc[i]
    # create folder
    pathlib.Path(f"./orca_minima_opt/reaction-{i}/").mkdir(parents=True, exist_ok=True)
    # copy xyz files
    shutil.copyfile(f"./optimised_aligned_xyz_files/reaction-{i}/reaction-{i}-rct-xtb.xyz",
                    f"./orca_minima_opt/reaction-{i}/reaction-{i}-rct-xtb.xyz")
    shutil.copyfile(f"./optimised_aligned_xyz_files/reaction-{i}/reaction-{i}-prod-xtb.xyz",
                    f"./orca_minima_opt/reaction-{i}/reaction-{i}-prod-xtb.xyz")
    # write input files
    with open(f"orca_minima_opt/reaction-{i}/reaction-{i}-rct-pbeh3c-orca_opt.inp", "w") as fh:
        fh.write(
            template.replace("xyzfile 0 1 template.xyz",
                             f"xyzfile {charge} {mult} reaction-{i}-rct-xtb.xyz")
        )
    with open(f"orca_minima_opt/reaction-{i}/reaction-{i}-prod-pbeh3c-orca_opt.inp", "w") as fh:
        fh.write(
            template.replace("xyzfile 0 1 template.xyz",
                             f"xyzfile {charge} {mult} reaction-{i}-prod-xtb.xyz")
        )
    


