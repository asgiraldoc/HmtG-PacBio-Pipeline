import sys
import os
import argparse
import subprocess

# Add script directory to path to find custom modules
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_dir, 'scripts'))


## import functions
from readsRedirection import primerDetection
from mafft import mafftRaw, mafftFinal, mafftHap
from fasta2binary import fasta2bin
from VAEmethod import VAE_model
from DBScan import extract_cluster_labels_dbscan
from cluster2fasta import txt2fasta
from consensus import cons
from rmTmp import remove_temp_files
from concatenate import concat
from corrHap import correct_sequences
from removeGap import remove_gaps_from_multifasta
from gapFree import remove_gap_columns
from countHap import countHaplotypes
from localBlast import make_blast_db, run_blast
import summary


def main():
    ## Arguments
    parser = argparse.ArgumentParser(description='Haemosporidian Mitochondrial Genome PacBio Pipeline (HmtG-PacBio Pipeline)')
    ### main arguments
    parser.add_argument('-rR', '--rawReads', type=str, help="rawReads from PacBio sequencing", required=True)
    parser.add_argument('-pF', '--primerF', type=str, help="primerF 5'-3', default='GATTCTCTCCACACTTCAATTCGTACTTC'", default='GATTCTCTC')
    parser.add_argument('-pR', '--primerR', type=str, help="primerR 3'-5', default='GAAGTACGAATTGAAGTGTGGAGAGAATC'", default='AGACCGAACCTTGGACTC')
    parser.add_argument('-eps', '--epsDBScan', type=float, help="epsilon value for DBScan clustering, default=1.0", default=1.0)
    parser.add_argument('-rF', '--RemoveFiles', type=str, help="Removing temporal files, default=yes", default='yes')
    parser.add_argument('-rB', '--blastn', type=str, help="Run blastn locally, default=yes", default='yes')

    args = parser.parse_args()

    ## files
    rawReads = args.rawReads
    nameSample = os.path.splitext(os.path.basename(rawReads))[0]

    ## run readsRedirection
    primerF = args.primerF
    primerR = args.primerR
    primerDetection(rawReads, primerF, primerR)

    rmFiles = args.RemoveFiles

    ## run raw aligment
    mafftRawOut_name = nameSample + "_mafftRaw.fasta"
    no_long_exists = any(f.endswith("_mafftRaw.fasta") for f in os.listdir())
    if not no_long_exists:
        print("Running first alignment...")
        mafftRawIn = nameSample + "_nolong.fasta"
        mafftRaw(mafftRawIn)
    else:
        print("A file with extension '_mafftRaw.fasta' was found, no initial alignment is required.")

    ## run convert DNA seq to Binary format
    bin_out_name = nameSample + "_bin.txt"
    no_long_exists = any(f.endswith("_bin.txt") for f in os.listdir())
    if not no_long_exists:
        fasta2bin(mafftRawOut_name)
        print("Converting DNA into bytes...")
    else:
        print("A file with extension '_bin.txt' was found, no convertion is required.")

    ## run VAE program and clustering
    epsilon = args.epsDBScan
    mu, VAErunData = VAE_model(bin_out_name, epsilon)
    extract_cluster_labels_dbscan(mu, VAErunData, nameSample, epsilon)

    ## run cluster2fasta
    txtCluster = [f for f in os.listdir() if f.endswith('-.txt') and f.startswith(nameSample)]
    for headers_file in txtCluster:
        mapped_output_file = headers_file.split(".")[0] + ".fa"
        txt2fasta(mafftRawOut_name, headers_file, mapped_output_file)

    print("Running last alignment...")
    ## run final aligment
    filesM = [f for f in os.listdir() if f.endswith('.fa') and f.startswith(nameSample)]
    mafftFinal(filesM)

    ## consensus output
    filesC = [f for f in os.listdir() if f.endswith('_mafftFinal.fasta') and f.startswith(nameSample)]
    cons(filesC)

    ## concatenate output
    filesC0  = [f for f in os.listdir() if f.endswith('_mafftFinal.fasta') and f.startswith(nameSample)]
    filesC1  = [f for f in os.listdir() if f.endswith('_consensus.fasta')  and f.startswith(nameSample)]
    concat(filesC1, filesC0)

    ## gapfree output
    filesG0  = [f for f in os.listdir() if f.endswith('-_RawHap.fasta')]
    for file in filesG0:
        outf = str(file).split("-")[0] + "-_RawHapng.fasta"
        remove_gaps_from_multifasta(file, outf)

    ### mafft gapfree
    filesM1 = [f for f in os.listdir() if f.endswith('-_RawHapng.fasta')]
    mafftHap(filesM1)

    ## correcting Haplotype alignment
    filesHc = [f for f in os.listdir() if f.endswith('-_aliHap.fasta')]
    for file in filesHc:
        outf = str(file).split("-")[0] + "-_corrHap.fasta"
        correct_sequences(file, outf)

    ## Haplotypes gapfree output
    filesG1  = [f for f in os.listdir() if f.endswith('-_corrHap.fasta')]
    for file in filesG1:
        outf = str(file).split("-")[0] + "-_corrHapng.fasta"
        remove_gap_columns(file, outf, "no")

    ## counting Haplotypes
    filesH = [f for f in os.listdir() if f.endswith('-_corrHapng.fasta')]
    for file in filesH:
        outf = str(file).split("-")[0] + "_cluster.fasta"
        countHaplotypes(file, outf)

    ## distances summary
    dinstances = summary.calculate_all_distances()
    with open("summary_distances.tsv", "w") as f:
        f.write(dinstances)

    ## run local Blast
    if args.blastn == 'yes' or args.blastn == 'y' or args.blastn == 'Yes' or args.blastn == 'Y':
        print("Running local blastn...")
        blast_db_base = os.path.join(script_dir, 'blast', 'HmtG_database_PacBio')
        blast_db_fasta = blast_db_base + '.fasta'
        make_blast_db(blast_db_fasta, 'nucl', blast_db_base)
        run_blast('.', blast_db_base)


    # removing temporal files
    remove_temp_files(rmFiles)

if __name__ == '__main__':
    main()
