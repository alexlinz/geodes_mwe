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

genome = sys.argv[1]    
taxonFile = 'Readme.csv'
inputGff = genome + '.gff'
outputGff = genome + '_parsed.gff'
outputTable = genome + '_table.txt'

#%%#############################################################################
### Update the inputGff file. Replace ID with 'locus tag' field
### Make a separate table with taxonomy and product name info
################################################################################

# Store the classification file as a dictionary

taxonFile = "Readme.csv"
readme = pandas.read_csv(taxonFile)
readme["TaxString"] = readme['Phylum'] + ';' + readme['Class'] + ';' + readme['Order'] + ';' + readme['Lineage'] + ';' + readme['Clade'] + ';' + readme['Tribe']
taxonDict = readme.set_index('IMG OID').to_dict()['TaxString']
   
# Read in the GFF file
# Each record contains all sequences belonging to the same contig
# For each sequence within the record, replace the ID with the locus_tag

inFile = open(inputGff, 'r')
outFile1 = open(outputGff, 'w')
outFile2 = open(outputTable, 'w')

for record in GFF.parse(inFile):
    for seq in record.features:
        seq.id = seq.qualifiers['locus_tag'][0] # this is a list for some reason
        product = seq.qualifiers['product'][0]
	del seq.qualifiers['locus_tag']
    GFF.write([record], outFile1)
taxonomy = taxonDict[genome] * len(seq.id)

outFile2.writelines(map("{},{},{}\n".format, seq.id, taxonomy, product))        
        
inFile.close()
outFile1.close()