# Calum Pennington (c.pennington@imperial.ac.uk)
# Nov 2016

# Basic population genomics - analysis of SNP (single-nucleotide polymorphism) data.
# Calculates:
#  genotype and allele frequencies
#  expected genotype frequencies.
# Tests for Hardy-Weinberg equilibrium.
# Identifies SNPs with big departures from Hardy-Weinberg equilibrium.

library(dplyr)
library(ggplot2)
library(reshape2)
# Load packages.

## View data
g <- read.table(file="../Data/H938_chr15.geno", header=TRUE)
# Read a file as a dataframe.

head(g)
dim(g)
# See top of dataframe and amount of data.
# 'head()' is useful to visualise dataframes and check new columns you make behave as you expect. Get in the habit of checking work with 'head()' as you go along.

## Calculate number of counts per locus
g <- mutate(g, nObs = nA1A1 + nA1A2 + nA2A2)
head(g)
# 'mutate()' (from 'dplyr') adds a function's result to a new column of a dataframe.
# Confirm 'g' has a new column, 'nObs'.

summary(g$nObs)
# Prints min, max, mean, median, quartiles.

pdf("../Results/nObs_Histogram.pdf")
print(qplot(nObs, data = g))
dev.off()
# Make a histogram of 'nObs' column.

## Calculate genotype and allele frequencies
g <- mutate(g, p11 = nA1A1/nObs, p12 = nA1A2/nObs, p22 = nA2A2/nObs )
# Genotype frequencies.

g <- mutate(g, p1 = p11 + 0.5*p12, p2 = p22 + 0.5*p12)
# Compute allele frequencies from genotype frequencies.
# The human genome is diploid – it has two sets of chromosomes. (Genotype describes the allele on each chromosome). An allele can be in homozygous or heterozygous state. It occurs twice in homozygous state (once per chromosome) – once in heterozygous state. Thus, the frequency of, eg allele A1, in a population, is 2*p11 + p12 = p11 + 0.5*p12.

head(g)

pdf("../Results/Allele_Frequency.pdf")
print(qplot(p1, p2, data=g))
dev.off()
# Plot frequency of major vs minor allele.

## Plotting genotype on allele frequencies
gTidy <- select(g, c(p1,p11,p12,p22)) %>%
  melt(id='p1',value.name="Genotype.Proportion")
head(gTidy)
dim(gTidy)
# Subset data by columns, and pass to 'melt()', which reformats data.
# Make a dataframe of the minor allele's frequency against each genotype's frequency, per SNP.
# 'gTidy' is 3 times as long as the number of SNPs in the data, as there are 3 possible genotypes per SNP.

# ggplot(gTidy) + geom_point(aes(x = p1,
#                                y = Genotype.Proportion,
#                                color = variable,
#                                shape = variable))

pdf("../Results/Genotype_vs_Allele_Freq.pdf")
print(ggplot(gTidy) +
  geom_point(aes(x=p1,y=Genotype.Proportion, color=variable,shape=variable)) +
  stat_function(fun=function(p) p^2, geom="line", colour="red",size=2.5) +
  stat_function(fun=function(p) 2*p*(1-p), geom="line", colour="green",size=2.5) +
  stat_function(fun=function(p) (1-p)^2, geom="line", colour="blue",size=2.5)
)
dev.off()
# Add lines representing Hardy-Weinberg (HW) proportions.

# The data do not perfectly fit Hardy-Weinberg proportions - there is systematic deficiency of heterozygotes and excess of homozygotes. Let's look at why.

## Testing Hardy-Weinberg
g <- mutate(g, X2 = (nA1A1-nObs*p1^2)^2 / (nObs*p1^2) +
              (nA1A2-nObs*2*p1*p2)^2 / (nObs*2*p1*p2) +
              (nA2A2-nObs*p2^2)^2 / (nObs*p2^2)) 

g <- mutate(g,pval = 1-pchisq(X2,1))
head(g)
head(g$pval) # See the top few p-values.
# Chi-squared test
# Compute the test statistic, then its p-value. Add the results to a new column of the dataframe.
# Chi-squared = sum of((observed i - expected i)^2 / expected i)

## Multiple testing problem
# As we test many, many SNPs, it is problematic, here, to reject the null hypothesis if p < 5%.
# We will do two checks to see if the data are globally consistent with the null.

sum(g$pval < 0.05, na.rm = TRUE)
# See how many tests have p < 0.05.

pdf("../Results/pval_Distribution_Check.pdf")
print(qplot(pval, data = g))
dev.off()
# Check p-values are uniformly distributed.
# p-values of a well-designed Chi-squared test should be uniformly distributed between 0 and 1 (Fisher).

pdf("../Results/Exp_vs_Obs_Hetero.pdf")
print(qplot(2*p1*(1-p1), p12, data = g) +
  geom_abline(intercept = 0, slope=1, color="red", size=1.5)
)
dev.off()
# Plot expected vs observed heterozygosity.

## Calculate mean deficiency of heterozygotes relative to expected proportion
pDefHet <- mean((2*g$p1*(1-g$p1)-g$p12) / (2*g$p1*(1-g$p1)))
pDefHet
# 'p12' is the observed frequency of heterozygotes.
# We can calculate expected genotype frequencies, using the HW equation (p^2 + 2pq + q^2) and observed allele frequencies.
# Expected frequency of heterozygotes is 2pq, where p and q are frequencies of two alleles.

## Find specific loci that are big departures from HW
g <- mutate(g, F = (2*p1*(1-p1)-p12) / (2*p1*(1-p1)))
# Compute the above deficiency per SNP. This is called F (Sewall-Wright).
# Add to the dataframe.

pdf("../Results/Hetero_Deficiency_perSNP.pdf")
print(plot(g$F, xlab = "SNP number"))
dev.off()
# Plot how the deficiency changes from one end of the chromosome to the other.

# A low/high F due to genotyping error likely affects only one SNP. A population genetic force, however, would affect multiple SNPs.
# So:

## Take a local average in a sliding window of SNPs.
movingavg <- function(x, n=5){stats::filter(x, rep(1/n,n), sides = 2)}
# Define a function, 'movingavg', with 2 arguments. Argument n's default value is 5.
# 'stats::filter' calls the filter function from the stats library.
# Take 5 values, centred on an SNP. Weigh them each by 1/5 and take the sum.
# Computes an average F over every 5 consecutive SNPs.

pdf("../Results/Sliding_Av_F.pdf")
print(plot(movingavg(g$F), xlab="SNP number"))
dev.off()
# Plot values of 'movingavg'.

outlier=which (movingavg(g$F) ==
                 max(movingavg(g$F),na.rm=TRUE))
g[outlier,]
# Assign to 'outlier', the row number of the maximum 'movingavg' value.
# Print the row.
# Extracts the SNP ID for the biggest F value.