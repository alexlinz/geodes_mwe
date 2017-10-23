###############################################################################
# CodeTitle.py
# Copyright (c) 2017, Joshua J Hamilton and Alex Linz
# Affiliation: Department of Bacteriology
#              University of Wisconsin-Madison, Madison, Wisconsin, USA
# URL: http://http://mcmahonlab.wisc.edu/
# All rights reserved.
################################################################################
# Make table of info from gff files
################################################################################

#%%#############################################################################
### Import packages
################################################################################

from BCBio import GFF # Python package for working with GFF files
import pandas
import os
import sys

#%%#############################################################################
### Define input files
################################################################################

# genome = sys.argv[1]
genome = "GCF_000149405.2_ASM14940v2_genomic"
taxonFile = 'algae_phylogeny.txt'
inputGff = genome + '.gff'
outputGff = genome + 'parsed.gff'
outputTable = genome + 'table.txt'

#%%#############################################################################
### Update the inputGff file. Replace ID with 'locus tag' field
### Make a separate table with taxonomy and product name info
################################################################################

# Store the classification file as a dictionary

readme = pandas.read_table(taxonFile, names = ["Genome", "Taxonomy"])
taxonDict = readme.set_index('Genome').to_dict()['Taxonomy']
taxonomy  = taxonDict[genome]

# Read in the GFF file
# Extract product information
# Rename genes including species name because they are just numbered

inFile = open(inputGff, 'r')
outFile1 = open(outputGff, 'w')
outFile2 = open(outputTable, 'w')

for record in GFF.parse(inFile, target_lines = 10):
    for seq in record.features:
        seq.qualifiers['ID'][0] = seq.qualifiers['locus_tag'][0]
        if 'product' in seq.qualifiers.keys():
          product = seq.qualifiers['product'][0]
        else:
          product = 'None given'
        print seq.id+'\t'+genome+'\t'+str(taxonomy)+'\t'+product+'\n'
        outFile2.write(seq.id+'\t'+genome+'\t'+str(taxonomy)+'\t'+product+'\n')
    GFF.write([record], outFile1)

inFile.close()
outFile1.close()
outFile2.close()
