from autode.geom import calc_rmsd
import pandas as pd
import glob
import os


def rmsd_from_file_names(filename1, filename2):
    
    
def get_dhs_gs_rmsd_and_total_iters(idx):
    dirname = f"dhs_gs/reaction-{idx}/"
    file_list = list(glob.glob(dirname+f"reaction-{idx}-dhs-gs.sh.e*"))
    if len(file_list) == 0:
        return None, None
        
    assert len(file_list) == 1
    outfile = file_list[0]
    with open(outfile) as fh:
        end_line = None
        for line in fh:
            if "Finished DHSGS procedure in" in line:
                end_line = line
                break
    
    if end_line is None:
        return None, None
    macro, micro = end_line.split()[6], end_line.split()[10]
    macro, micro = int(macro), int(micro)
    
    iters = macro + micro + 2
    
    xyzfile = dirname + f"dhsgs/DHSGS_ts_guess.xyz"
    ts_ref_file = 
    if not os.path.isfile(xyzfile):
        return None, None
    rmsd = rmsd_from_file_names(xyzfile, ts_ref_file)
    
    return rmsd, iters
    
    
def get_cineb_rmsd_and_total_iters(idx, image_num):
    dirname = f"ci_neb_5/reaction-{idx}/"
    
    orca_out_files = list(glob.glob(dirname+f"neb/*/*_orca.out"))
    iters = len(orca_out_files)
    
    # Check if optimisation successful
    if not os.path.isfile(dirname+"/neb/neb_optimised.xyz"):
        return None, None
    
    ts_ref_file = 
    xyzfile = dirname + f"cineb-{image_num}-peak.xyz"
    if not os.path.isfile(xyzfile):
        return None, None
    rmsd = rmsd_from_file_names(xyzfile, ts_ref_file)
    
    return rmsd, iters
    
row_names = [f"reaction-{idx}" for idx in range(0, 8)]
col_name_base = ["CINEB-5", "CINEB-10", "DHS-GS", "i-EIP"]
col_names_rmsd = [x+"_rmsd" for x in col_name_base]
df_rmsd = pd.DataFrame(np.zeros(shape=(8, 4)), rows = row_names, columns = col_names_rmsd)
col_names_iters = [x+"_iters" for x in col_name_base]
df_iters = pd.DataFrame(np.zeros(shape=(8, 4)), rows = row_names, columns = col_names_iters)
df_failures = pd.DataFrame(np.zeros(shape=(1, 4)), rows = ["Failures"], columns = col_names_base)


for i in range(0, 8):
    
    cineb5_rmsd, cineb5_iters = get_cineb_rmsd_and_total_iters(i, 5)
    df_rmsd.loc[i, "CINEB-5"] = cineb5_rmsd
    df_iters.loc[i, "CINEB-5"] = cineb5_iters
    
    cineb10_rmsd, cineb10_iters = get_cineb_rmsd_and_total_iters(i, 10)
    df_rmsd.loc[i, "CINEB-10"] = cineb10_rmsd
    df_iters.loc[i, "CINEB-10"] = cineb10_iters
    
    dhsgs_rmsd, dhsgs_iters = get_dhs_gs_rmsd_and_total_iters(i)
    df_rmsd.loc[i, "DHS-GS"] = dhsgs_rmsd
    df_iters.loc[i, "DHS-GS"] = dhsgs_iters
    