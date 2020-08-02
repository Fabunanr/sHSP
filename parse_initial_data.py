#!/usr/bin/env python
import sys, re
import pandas as pd

protein_list = [] #this creates a list of the protein names from phytozome blast output (fmt 10)

#This will read the blast output and puts protein name into list above
with open(sys.argv[1],'r') as f:
    blast_10 = f.readlines()
    for line in blast_10:
        # x = re.split(', |  |\*|\n',line)
        x = re.split('[,  ]',line) #using re, split text using comma and space
        # print(x)
        protein_list.append(x[1])

#Below removes duplicates
protein_list = list(dict.fromkeys(protein_list))
# print(protein_list)
# protein_list = ['AL1G60810.t1', 'Cagra.18351s0001.1','Migut.D01069.1', 'Potri.003G109200.2','Potri.003G109200.3','AT1G52560.1', 'AT1G52560.2']


# This is an automatically generated script to run your query
# to use it you will require the intermine python client.
# To install the client, run the following command from a terminal:
#
#     sudo easy_install intermine
#
# For further documentation you can visit:
#     http://intermine.readthedocs.org/en/latest/web-services/

# The following two lines will be needed in every python script:
from intermine.webservice import Service
service = Service("https://phytozome.jgi.doe.gov/phytomine/service")

full_table = []
problem_identifiers = []
def query_call(in_list):
    for prot in in_list:
        # print(prot)
        # Get a new query on the class (table) you will be querying:
        query = service.new_query("Protein")

        # The view specifies the output columns
        # query.add_view("CDSs.protein.sequence.residues","CDSs.sequence.residues")
        query.add_view(
            "CDSs.protein.sequence.residues", "organism.commonName", "organism.genus",
            "organism.species", "organism.taxonId", "organism.shortName", "genes.name", "genes.primaryIdentifier",
            "CDSs.sequence.residues",
        )

        # Uncomment and edit the line below (the default) to select a custom sort order:
        # query.add_sort_order("Protein.name", "ASC")
        query.add_constraint("name", "=", prot, code = "A")

        # for row in query.rows():
            # print(row["name"],row["CDSs.protein.sequence.residues"],row["CDSs.sequence.residues"])
        list = []
        for row in query.rows():
            # print(row["CDSs.protein.sequence.residues"], row["organism.commonName"], row["organism.genus"], \
                # row["organism.species"], row["organism.taxonId"], row["organism.shortName"],row["genes.name"], row["genes.primaryIdentifier"],
                 # row["CDSs.sequence.residues"] )
            # list.append(prot)
            list.append(row["organism.commonName"])
            list.append(row["organism.taxonId"])
            list.append(row["organism.shortName"])
            list.append(row["organism.genus"])
            list.append(row["organism.species"])
            list.append(row["genes.name"])
            list.append(row["genes.primaryIdentifier"])
            list.append(row["CDSs.sequence.residues"])
            list.append(row["CDSs.protein.sequence.residues"])
        if len(list) > 0:
            full_table.append(list)
        # elif len(list) > 8:
        #     print(len(list))
        else:
            problem_identifiers.append(prot+".p")
query_call(protein_list)

# print(problem_identifiers)
query_call(problem_identifiers)

clean_table = []
for i in full_table:
    if len(i) > 9:
        print(i[5],"is weird")
        clean_table.append(i[:9])
    else:
        clean_table.append(i)
# print(clean_table)


df = pd.DataFrame(clean_table, columns = ['Common Name','Taxon ID','Organism Short Name','Genus','Species','Gene Name','Gene - Primary Identifier','CDS','Protein Sequence'])
# df.sort_values('Taxon ID', inplace=True)
df.drop_duplicates(subset = "Gene Name", keep='first',inplace=True)
df.to_csv('out.csv',sep=',')
