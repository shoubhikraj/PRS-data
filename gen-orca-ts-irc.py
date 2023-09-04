import shutil
import os
import pathlib
import pandas as pd


df = pd.read_csv("reactions_to_bench.csv", header=0)

with open("orca-ts-irc-template.inp") as fh:
    template = fh.read()
    
def write_dhs_gs_ts_files(idx, charge, mult):
    prefix = f"dhs_gs/reaction-{idx}/"
    tsguess = prefix + "dhsgs/DHSGS_ts_guess.xyz"
    tsopt_folder = prefix + "ts-opt/"
    tsinp_base = f"reaction-{idx}-dhsgs_optts"
    if not os.path.isfile(tsguess):
        return None
    
    pathlib.Path(tsopt_folder).mkdir(exist_ok=True)
    
    shutil.copyfile(tsguess, tsopt_folder+"DHSGS_ts_guess.xyz")
    text = template.replace("*xyzfile 0 1 template.xyz", f"*xyzfile {charge} {mult} DHSGS_ts_guess.xyz")
    text = text.replace("inpfile", tsinp_base)
    
    with open(tsopt_folder+tsinp_base+".inp", "w") as fh:
        fh.write(text)

    return None
    
def write_cineb_ts_files(idx, num, charge, mult):
    prefix = f"ci_neb_{num}/reaction-{idx}/"
    tsguess = prefix + f"cineb-{num}-peak.xyz"
    tsopt_folder = prefix + "ts-opt/"
    tsinp_base = f"reaction-{idx}-cineb{num}_optts"
    if not os.path.isfile(tsguess):
        return None
        
    pathlib.Path(tsopt_folder).mkdir(exist_ok=True)
    
    shutil.copyfile(tsguess, tsopt_folder+f"cineb-{num}-peak.xyz")
    text = template.replace("*xyzfile 0 1 template.xyz", f"*xyzfile {charge} {mult} cineb-{num}-peak.xyz")
    text = text.replace("inpfile", tsinp_base)
    
    with open(tsopt_folder+tsinp_base+".inp", "w") as fh:
        fh.write(text)

    return None
    
def write_ieip_ts_files(idx, charge, mult):
    prefix = f"i_eip/reaction-{idx}/"
    tsguess = prefix + "ieip/IEIP_ts_guess.xyz"
    tsopt_folder = prefix + "ts-opt/"
    tsinp_base = f"reaction-{idx}-ieip_optts"
    if not os.path.isfile(tsguess):
        return None
    
    pathlib.Path(tsopt_folder).mkdir(exist_ok=True)
    
    shutil.copyfile(tsguess, tsopt_folder+"IEIP_ts_guess.xyz")
    text = template.replace("*xyzfile 0 1 template.xyz", f"*xyzfile {charge} {mult} IEIP_ts_guess.xyz")
    text = text.replace("inpfile", tsinp_base)
    
    with open(tsopt_folder+tsinp_base+".inp", "w") as fh:
        fh.write(text)

    return None

for i in range(0, 8):
    charge = df["charge"].iloc[i]
    mult = df["multiplicity"].iloc[i]
    
    #DHSGS
    write_dhs_gs_ts_files(i, charge, mult)
    
    # CI-NEB(5)
    write_cineb_ts_files(i, 5, charge, mult)
    
    # CI-NEB(10)
    write_cineb_ts_files(i, 10, charge, mult)
    
    # i-EIP
    write_ieip_ts_files(i, charge, mult)
    


