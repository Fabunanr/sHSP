import sys, csv
from Bio import SeqIO, SearchIO

# This python script will:
#(1) parse a tab delmited blast output file
#(2) get the sequence hit in the protein fasta file
#(3) get the sequence hit in the cds fasta file
#(4) make a fasta file for the protein and cds seuqnces seperately

protein_file = open(sys.argv[1],'r')
cds_file = open(sys.argv[2], 'r')

name = sys.argv[4]

protein_fasta_out = str(name+'_pep.fa')
cds_fasta_out = str(name+'_cds.fa')

blast_hits_list = []
with open(sys.argv[3],'r') as blast_hits:
    hit_reader = csv.reader(blast_hits, delimiter='\t')
    for hit in hit_reader:
        # print(hit[1])
        if hit[1] not in blast_hits_list:
            blast_hits_list.append(hit[1])

def get_sequences(prot_or_cds_infile,prot_or_cds_outfile):
    fasta_sequences = SeqIO.parse(prot_or_cds_infile, 'fasta')
    with open(prot_or_cds_outfile,'w') as out:
        for seq in fasta_sequences:
            if seq.id in blast_hits_list:
                SeqIO.write(seq,out,'fasta-2line')

get_sequences(protein_file,protein_fasta_out)
get_sequences(cds_file,cds_fasta_out)
