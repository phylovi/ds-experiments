import libsbn
import vip.burrito
import pandas as pd
import argparse
import os

parser = argparse.ArgumentParser(description='A script to train SBN via gradients.')
parser.add_argument('ds_path', type=str, 
                    help='Path to ds-experiments.')
parser.add_argument('-o', type=str, default="_ignore/", 
                    help='Path to write outputs.')

args = parser.parse_args()

data_sets = {
    "ds1": "DS1/DS1_out.t",
    "fixed_ds1": "fixed_DS1/fixed_DS1_out.t",
    "ds4": "DS4/DS4_out.t"
}

fasta_paths = {
    "ds1": "DS1/DS1.fasta",
    "fixed_ds1": "fixed_DS1/fixed_DS1.fasta",
    "ds4": "DS4/DS4.fasta"
}

data_set = "fixed_ds1"

if not os.path.exists(data_sets[data_set]):
    raise SystemExit(f"Error: {data_sets[data_set]} is missing.")
if not os.path.exists(fasta_paths[data_set]):
    raise SystemExit(f"Error: fasta file {fasta_paths[data_set]} is missing.")

burn_in_fraction = 0
num_particles = 10
branch_model_name="split"
scalar_model_name="lognormal"
optimizer_name="simple"
phylo_model_specification = libsbn.PhyloModelSpecification(
    substitution="JC69", site="constant", clock="strict"
)

burro = vip.burrito.Burrito(
    mcmc_nexus_path=f"{args.ds_path}/{data_sets[data_set]}",
    burn_in_fraction=0,
    fasta_path=f"{args.ds_path}/{fasta_paths[data_set]}",
    phylo_model_specification=phylo_model_specification,
    branch_model_name=branch_model_name,
    scalar_model_name=scalar_model_name,
    optimizer_name=optimizer_name,
    particle_count=num_particles)

step_count = 10000
burro.gradient_steps(step_count)

if not os.path.exists(args.o):
    os.makedirs(args.o)

elbo_trace = pd.DataFrame({"elbo": burro.elbo_trace})
prefix = f"{args.o}/{data_set}-loop{step_count}"
elbo_trace.to_csv(prefix+"-elbo_trace.csv", header=False)
print("Marginal likelihood: %f" % burro.marginal_likelihood_estimate(1000))
burro.inst.sbn_parameters.tofile(prefix+"-parameters.csv", ",")
