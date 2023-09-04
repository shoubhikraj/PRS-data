import shutil
import pathlib
import pandas as pd


df = pd.read_csv("reactions_to_bench.csv", header=0)

with open("orca-neb-template.inp") as fh:
    template = fh.read()

for i in range(0, 8):
    charge = df["charge"].iloc[i]
    mult = df["multiplicity"].iloc[i]
    # create folder
    pathlib.Path(f"./orca_neb_ref/reaction-{i}/").mkdir(parents=True, exist_ok=True)
    # copy xyz files
    shutil.copyfile(f"./final_aligned_orca_opt/reaction-{i}/reaction-{i}-rct-orca.xyz",
                    f"./orca_neb_ref/reaction-{i}/reaction-{i}-rct-orca.xyz")
    shutil.copyfile(f"./final_aligned_orca_opt/reaction-{i}/reaction-{i}-prod-orca.xyz",
                    f"./orca_neb_ref/reaction-{i}/reaction-{i}-prod-orca.xyz")
    # write input file
    with open(f"orca_neb_ref/reaction-{i}/reaction-{i}-pbeh3c-orca_neb.inp", "w") as fh:
        txt = template.replace("xyzfile 0 1 reactant.xyz",
                               f"xyzfile {charge} {mult} reaction-{i}-rct-orca.xyz")
        txt = txt.replace("product.xyz",
                          f"reaction-{i}-prod-orca.xyz")
        fh.write(txt)
    


