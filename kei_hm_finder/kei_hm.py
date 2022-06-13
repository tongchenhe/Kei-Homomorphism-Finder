'''
   Module name: kei_hm.py
   Author: Tongchen He
   Date created: 12/22/2021
   Date last modified: 5/13/2022
'''

from itertools import combinations, permutations
from copy import copy


# Given a quandle and its rank, find all the generators of the quandle
def generator_finder(rank, q1):
    qnd = q1
    list_of_gen = []
    # store all the rank-# combinations of 0-len(q) in a tuple for testing
    tup = list(combinations([i for i in range(len(qnd))], rank))
    for eles in tup:
        generated_eles = list(eles)
        count = 0
        while True:
            count+=1
            old_eles = copy(generated_eles)
            for e1 in generated_eles:
                for e2 in generated_eles:
                    if count <= 1 or e2 not in old_eles:
                        if not qnd[e1][e2] in generated_eles:
                            generated_eles.append(qnd[e1][e2])
                        if not qnd[e2][e1] in generated_eles:
                            generated_eles.append(qnd[e2][e1])
            if len(old_eles) == len(generated_eles):
                break

        if len(generated_eles) == len(qnd):
            list_of_gen.append(eles)
    return list_of_gen


#Function to search for homomorphisms from the fundamental group to the symmetric group.
def homomorphism_finder(seed_strand_set, knot_dict, gnr, q1):
    #Get all permutations of the seed strand set
    perms_of_seed_strands=list(permutations(seed_strand_set))
    #Set initial value of "We have found a homomorphism" to "No"
    hmorph=False
    all_generators = gnr
    #Run through every generating set in the quandle
    for gen_set in all_generators:
        #Run through every permutation of the seed strand set
        for perm in perms_of_seed_strands:
            #Map each seed strand to a generator
            qnd_gen_set = generator_assign(perm, gen_set)
            #Map every strand to a generator
            mapping = strand_assignment(qnd_gen_set, knot_dict, q1)
            #Determine if that mapping admits a surjective homomorphism
            hmorph = hom_tester(mapping, knot_dict, q1)
            #If it does...
            if hmorph:
                #Return the Boolean variable indicating that it does and the seed-strand-to-generator mapping that produced it
                return hmorph, qnd_gen_set
    #If no hm was found across all permutations, hmorph will be false and we don't care what the program thinks the sym_gen_set is
    return hmorph, qnd_gen_set


def strand_assignment(qnd_gen_set, knot_dict, q1):
    mapping = qnd_gen_set.copy()

    #This variable will indicate when all strands that can be assigned a generator have been assigned a generator
    new_assignment=True
    #while we aren't done
    while new_assignment:
        #This iteration will be the last one unless told otherwise
        new_assignment=False
        #Scan through each overstrand in the knot dictionary
        for overstrand in knot_dict:
            #If the overstrand has been assigned a mapping...
            if overstrand in mapping:
                #Scan through all its understrand pairs (there may be more than one if the strand is the overstrand of more than one crossing)
                for understrands in knot_dict[overstrand][1]:
                    #If both understrands of this particular crossing have been assigned...
                    if understrands[0] in mapping and understrands[1] in mapping:
                        #This crossing has been fully assigned and we're done here
                        pass
                    #If only the first understrand has been assigned...
                    elif understrands[0] in mapping:
                        #Then add the second understrand to mapping, assigning it to a (possibly) new transposition
                        mapping[understrands[1]]=q1[mapping[understrands[0]]][mapping[overstrand]]
                        #A new assignment has been made, so another iteration is necessary to make sure all possible assigments have been made
                        new_assignment=True
                    #If only the second understrand has been assigned...
                    elif understrands[1] in mapping:
                        #Then add the first understrand to mapping, assigning it to a (possibly) new transposition
                        mapping[understrands[0]] = q1[mapping[understrands[1]]][mapping[overstrand]]
                        #A new assignment has been made, so another iteration is necessary to make sure all possible assigments have been made
                        new_assignment=True
                    #Otherwise, neither understrand has yet been assigned a transposition, so let another iteration happen
            #Otherwise, the overstrand has not been assigned a mapping yet, and there is nothing we can do yet, so let another iteration happen
    #Return mapping, a dictionary with all strands that can be assigned a transpsition as keys, and their corresponding two-tuple transpositions as entries.
    return mapping

def generator_assign(perm, gen_set):
    #Defining dictionary to house generating set of transpositions
    qnd_gen_set={}
    #run through each element of the permuted seed strand set
    for i in range(len(perm)):
        #Add an entry to the generating set dictionary with the letter of the seed strand from the knot dictionary as the key and the quandle generator as the entry
        qnd_gen_set[perm[i]]=gen_set[i]
    #return the generating set, a dictionary with the keys being the seed strand letters and the entries being the quandle generators assigned to them
    return qnd_gen_set


def hom_tester(mapping, knot_dict, q1):
    if len(mapping) != len(knot_dict):
        return False
    for overstrand in knot_dict:
        #Scan through all its understrand pairs
        for understrands in knot_dict[overstrand][1]:
            #If ever one of the understrands' generators (it dosen't matter which understrand, since we're working with two-cycles. Otherwise, it would) does not equal the
            #Transpose product of the overstrand and other understrand, the Wirtinger relation does not hold for this crossing, and this is not a homomorphism.
            if mapping[understrands[0]] != q1[mapping[understrands[1]]][mapping[overstrand]]:
                #Return a False value
                return False
    #If the function has not been exited yet, then we have a valid homomorphism
    return True


