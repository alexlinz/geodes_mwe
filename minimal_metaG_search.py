###############################################################################
# CodeTitle.py
# Copyright (c) 2017, Joshua J Hamilton
# Affiliation: Department of Bacteriology
#              University of Wisconsin-Madison, Madison, Wisconsin, USA
# URL: http://http://mcmahonlab.wisc.edu/
# All rights reserved.
################################################################################
# Make Alex's code faster!
################################################################################

#%%#############################################################################
### Import packages
################################################################################

from BCBio import GFF # Python package for working with GFF files

#%%#############################################################################
### Define input files
################################################################################
    
taxonFile = 'minimal.contig.classification.txt'
productFile = 'minimal.product_names'
inputGff = 'minimal_metaG.gff'
outputGff = 'output.gff'

#%%#############################################################################
### Update the inputGff file. Replace ID with 'locus tag' field and add two 
### new fields containing the taxonomy and gene product information.
################################################################################

# Store the classification file as a dictionary
taxonDict = {}
with open(taxonFile, 'r') as inFile:
    for line in inFile:
       (key, val) = line.strip().split('\t') # Remove terminal new-line and split on the tab
       taxonDict[key] = val
   
# Store the gene product name file as a dictionary
productDict = {}
with open(productFile, 'r') as inFile:
    for line in inFile:
       (key, val, KO) = line.strip().split('\t') # Remove terminal new-line and split on the tab
       productDict[key] = val
       
# Read in the GFF file
# Each record contains all sequences belonging to the same contig
# For each sequence within the record, replace the ID with the l

inFile = open(inputGff, 'r')
outFile = open(outputGff, 'w')

for record in GFF.parse(inFile):
    for seq in record.features:
        seq.id = seq.qualifiers['locus_tag'][0] # this is a list for some reason
        del seq.qualifiers['locus_tag']
        seq.qualifiers['Taxonomy'] = taxonDict[record.id] # ID of record/contig
        seq.qualifiers['Product'] = productDict[seq.id] # ID of sequence/gene
    GFF.write([record], outFile)
        
inFile.close()
outFile.close()
