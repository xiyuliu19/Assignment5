#!/usr/bin/python
import sys
import fileinput
import re
import json

Lookup_geneID={}

for line in fileinput.input(['/home/xiyuliu/Assignment5/Homo_sapiens.GRCh37.75.gtf']):
    gene_id_matches = re.findall('gene_id \"(.*?)\";',line)
    gene_name_matches = re.findall('gene_name \"(.*?)\";',line)
    text_in_columns = re.split('\t',line)
    if len(text_in_columns)>3:
       if text_in_columns[2] == "gene":
          if gene_id_matches:
             if gene_name_matches:
                Lookup_geneID[gene_id_matches[0]] = gene_name_matches[0]

if len(sys.argv) < 2 or sys.argv[1][:2] != '-f' or len(sys.argv[1]) < 3 or not sys.argv[1][2] or not sys.argv[1][2].isdigit():
    column_number = 1
else:
    column_number = int(sys.argv[1][2])

Your_file = sys.argv[-2] if sys.argv[-1][0] == '>' else sys.argv[-1]

for line in fileinput.input(Your_file):
    text_in_columns = re.split(',',line)
    if text_in_columns[0] == '""':
       print line[:-1]
       continue
    id = re.split('\.', text_in_columns[column_number -1])[0].strip('"')
    if id in Lookup_geneID:
       text_in_columns[4]=re.sub('\n','',text_in_columns[4].rstrip());
       print text_in_columns[0] + "," + '"' +  Lookup_geneID[id] + '"' + "," + text_in_columns[2] + "," + text_in_columns[3] + "," + text_in_columns[4]
