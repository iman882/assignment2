from Bio.SeqFeature import SeqFeature, FeatureLocation
from Bio import SeqIO
from Bio.Seq import Seq
from os import mkdir, path, listdir


input_directory = "./fav_proteins1"  
output_file_fasta = "./output1/combined-proteins.faa"  
output_file_genbank = "./output1/combined-proteins.gb"  


with open(output_file_fasta, "w") as combined_fasta:
    for file_name in listdir(input_directory): 
        if file_name.endswith(".faa"):  
            file_path = f"{input_directory}/{file_name}"
            print(f"Processing file: {file_path}")
            with open(file_path, "r") as fasta_file:
                content = fasta_file.read().strip()
                if content.startswith(">"): 
                    combined_fasta.write(content + "\n")
                else:
                    print(f"Skipping invalid file: {file_name}")


records = []
for record in SeqIO.parse(output_file_fasta, "fasta"):

    record.seq.alphabet = IUPAC.protein

  
    record.annotations["molecule_type"] = "protein"
    record.annotations["topology"] = "linear"  # Required for GenBank format
    record.annotations["organism"] = "Unknown organism"  # Add placeholder organism

    
    source_feature = SeqFeature(FeatureLocation(0, len(record.seq)), type="source")
    record.features.append(source_feature)

  
    records.append(record)


if records:
    with open(output_file_genbank, "w") as genbank_file:
        SeqIO.write(records, genbank_file, "genbank")
    print(f"Converted {output_file_fasta} to {output_file_genbank}")
else:
    print("No valid records were found")

