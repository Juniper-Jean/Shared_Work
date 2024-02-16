Overview of Week6 Contents

Genomics and Bioinformatics
November 7-11 2016

/Code
Prac2_Pop_Gen.R - Analysis of SNP data, 'H938_chr15.geno'.
 Calculates genotype and allele frequencies.
 Tests for Hardy-Weinberg equilibrium.
 Identifies SNPs with big departures from Hardy-Weinberg equilibrium.


/Data
H938_chr15.geno - SNPs from chromosome 15 sampled from 52 global human populations (derived from the Human Genome Diversity project). Data for 'Prac2_Pop_Gen.R'.


/Reports
2_Basic_pop_genomics_2016.odt - Practical 2 handout, 'Basic population genomics using R', with questions answered.


/Results
'Prac2_Pop_Gen.R' outputs:
	nObs_Histogram.pdf - Histogram of observations of each SNP.

	Allele_Frequency.pdf - Frequency of major vs minor allele.

	Genotype_vs_Allele_Freq.pdf - The minor allele's frequency plotted against each genotype's frequency, per SNP.

	pval_Distribution_Check.pdf - Distribution of p-values from Chi-squared tests for deviation from Hardy-Weinberg proportions.

	Exp_vs_Obs_Hetero.pdf - Plot of Hardy-Weinberg-expected against observed heterozygosity.

	Hetero_Deficiency_perSNP.pdf - Deficiency of heterozygotes relative to the Hardy-Weinberg-expected proportion, per SNP.

	Sliding_Av_F.pdf - Average deficiency (F) for every 5 consecutive SNPs.
