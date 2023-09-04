optimise-align-xyz.py: Loads xyz files of reactants and products with autodE, optimises with xTB, and then aligns them by removing translational and rotational degrees of freedom

gen-orca-opt.py: Generates orca input files, using the template, for minimisation of the end points (reactant and product). These xyz files are used later.
realign-geometries.py: Aligns the orca optimised xyz files for all calculations

gen-cineb5-ade-input.py: Generate CI-NEB input scripts for autodE with 5 images
gen-cineb10-ade-input.py: Generate CI-NEB input scripts for autodE with 10 images
gen-dhs-gs-ade-input.py: Generate DHS-GS input scripts for autodE with 

gen-orca-neb.py: Generates orca input files for reference CI-NEB calculation, with 20 images
gen-orca-ts-opt.py: Generates orca input files for reference TS optimisation calculation, with converged CI-NEB image

analyse-output-files.py: Generates a csv file by analysing RMSD of TS guesses against the ORCA converged TS from different methods.