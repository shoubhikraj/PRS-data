import shutil
import pathlib
import pandas as pd


df = pd.read_csv("reactions_to_bench.csv", header=0)

with open("orca-ts-template.inp") as fh:
    template = fh.read()

for i in range(0, 8):
    charge = df["charge"].iloc[i]
    mult = df["multiplicity"].iloc[i]
    # create folder
    pathlib.Path(f"./orca_ts_opt_from_neb_ref/reaction-{i}/").mkdir(parents=True, exist_ok=True)
    # copy xyz files
    try:
        shutil.copyfile(f"./orca_neb_ref/reaction-{i}/reaction-{i}-pbeh3c-orca_neb_NEB-CI_converged.xyz",
                        f"./orca_ts_opt_from_neb_ref/reaction-{i}/"
                         f"reaction-{i}-pbeh3c-orca_neb_NEB-CI_converged.xyz")
    except FileNotFoundError:
        pass

    # write input file
    with open(f"orca_ts_opt_from_neb_ref/reaction-{i}/reaction-{i}-pbeh3c-orca_optts.inp", "w") as fh:
        txt = template.replace("xyzfile 0 1 template.xyz",
                               f"xyzfile {charge} {mult} "
                               f"reaction-{i}-pbeh3c-orca_neb_NEB-CI_converged.xyz")
        fh.write(txt)
    


