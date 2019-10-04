# Installation and Usage instructions
*This is a program called ensg2hugo.py that **takes a comma-delimited file as an argument** and **a column number as an input**, and **print a file where the Ensembl gene name has become a HUGO name**.*
***
1. Create a new directory called "Assignment5" in the home directory `mkdir Assignment5`  
2. `cd Assignment5`  
3. To get Homo_sapiens.GRCh37.75.gtf:<br>
As this file is too large, users can use **curl** to get it. `curl -O http://ftp.ensembl.org/pub/release-75/gtf/homo_sapiens/Homo_sapiens.GRCh37.75.gtf.gz`
4. Users can use **wget** or **curl** to get the file they want to work with. Here, take the unit test for an example, the command line is `wget https://github.com/davcraig75/unit/expres.anal.csv`  
or `curl -O https://github.com/davcraig75/unit/expres.anal.csv`  
Here, users will have these two files in the Assignment5 directory. Users can check it by type `ls -l` command.  
***
### Create script `vim ensg2hugo.py`  
```python
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
       print ','.join(text_in_columns)[:-1]
       continue
    id = re.split('\.', text_in_columns[column_number -1])[0].strip('"')
    if id in Lookup_geneID:
       text_in_columns[-1]=re.sub('\n','',text_in_columns[-1].rstrip());
       print ','.join(text_in_columns[:column_number-1]) + "," + '"' + Lookup_geneID[id] + '"' + "," + ','.join(text_in_columns[column_number:])
```
`chmod 755 ensg2hugo.py`  
Now, I can test this program by the unit test file. `./ensg2hugo.py -f2 expres.anal.csv >expres.anal.hugo.csv`  
There will print a file called "expres.anal.hugo.csv" in the Assignment5 directory, which the Ensembl gene name has become a HUGO name.  
***
:blush:Users can install this program by using **`git clone`**  
The command to run this program should like **`./ensg2hugo.py -f[0-9] Your_file.csv >Your_file.hugo.csv`**  
**Notably, users allow an option “-f [0-9]” where -f2 would pick the 2nd column where should be the gene_id. If there is no “-f” then the program will default the first column as the gene_id column.**    
Now, users can print the target file successfully!
