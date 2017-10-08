#!/bin/bash

awk -F'\t' -v OFS='\t' '{print $1,$2,$3,$4,$5,$6,$7,$8}' minimal_metaG.gff > part1.txt #split by first 8 columns - metagenome assembly has issue with whitespace in the fields.
awk -F'\t' '{print $9}' minimal_metaG.gff > part2.txt #put the last column of tags in its own file

awk -F";" '{for(i=1;i<=NF;i++){if ($i ~ /locus_tag=*/){print $i}}}' part2.txt > locust.txt
#These files have the relevant info in locustag instead of id
awk '{print substr($1,11)}' locust.txt > IDS.txt
# from product name file
while read line;
  do grep -wF $line minimal.product_names;
  done < IDS.txt > gene.txt
awk -F'\t' '{print $2}' gene.txt > product.txt

rows=$(wc -l minimal_metaG.gff | awk '{print $1}')
yes $metaG | head -n $rows > genome.txt
#look up phylogeny and make that column, too

while read line; do echo $line | cut -c1-18; done < IDS.txt > contigs.txt
sed -i -e 's/^$/NA/' contigs.txt
while read line;
  do line2=`grep -wF "$line" minimal.contig.classification.txt`;
  [ ! -z "$line2" ] && echo $line2 || echo "NA   No_classification"
  done < contigs.txt > class.txt
  
awk '{print $2}' class.txt > classification.txt

#add the ID tag back in
sed -i -e 's/^/ID=/' IDS.txt

awk -F'\t' '{print $4}' minimal_metaG.gff > start.txt #get the gene start location
paste -d "\t" part1.txt IDS.txt > cat1.txt #paste first 8 columns to ID tag
paste -d "," cat1.txt start.txt > cat2.txt #paste start location to ID
paste -d "," cat2.txt genome.txt > cat3.txt #paste genome to ID
paste -d "," cat3.txt classification.txt > cat4.txt #paste phylogeny to ID
paste -d "," cat4.txt product.txt > new.gff #paste product name to ID

