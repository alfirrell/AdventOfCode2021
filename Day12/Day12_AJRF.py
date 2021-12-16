import numpy as np
import pandas as pd

def prep_data(file_path):

    input = pd.read_csv(file_path, sep = "-", header=None, names = ["from", "to"])
    all_nodes = pd.Series.append(input["from"], input["to"]).unique()
    all_nodes = pd.DataFrame({"node": all_nodes})
    all_nodes["is_large"] = [node.isupper() for node in all_nodes["node"]]
    all_nodes

    input_both = pd.concat([input, pd.DataFrame({"from": input["to"], "to": input["from"]}) ], ignore_index=True)
    input_both = input_both[(input_both["from"] != "end") & (input_both["to"] != "start")]
    return(input_both)

def extend_chain(chain):
    prev_node = chain[-1]
    links = input_both[input_both["from"]==prev_node]["to"].values

    new_chains = [chain + [link] for link in links if link.isupper() or not(link in chain)]
    return(new_chains)

def get_chains(chain, complete_chains):
    new_chains = extend_chain(chain)
    for new_chain in new_chains:
        if new_chain[-1] == "end":
            #print(new_chain)
            complete_chains.append(new_chain)
        else:
            get_chains(new_chain, complete_chains)
    return(complete_chains)

input_both = prep_data("Day12/test_input1.txt")
complete_chains = get_chains(["start"], [])

print("# paths:", len(complete_chains))

## Part 2
## Allow one small cave to be visited twice - tweak the extend_chain function
def extend_chain(chain):
    prev_node = chain[-1]
    links = input_both[input_both["from"]==prev_node]["to"].values

    # Check if any small cave already visited twice.  If so, no more.
    lower_twice_already = False
    for chain_link in chain:
        if chain_link.islower() and chain.count(chain_link) >= 2:
            lower_twice_already = True

    ## Can add the link if: 
    # is upper case, 
    # is lower and not already in the chain, 
    # or is lower, in the chain, but no other small cave already visited
    new_chains = [chain + [link] for link in links if link.isupper() \
                                                    or chain.count(link) == 0 \
                                                    or (chain.count(link) == 1 and not(lower_twice_already))]
    return(new_chains)

input_both = prep_data("Day12/input_AJRF.txt")
# Care: this takes a few minutes for the full input - needs tuning!
complete_chains = get_chains(["start"], [])
print("# paths:", len(complete_chains))