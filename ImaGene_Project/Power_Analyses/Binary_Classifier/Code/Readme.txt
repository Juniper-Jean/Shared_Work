.md (Markdown) file?


#----
# Naming Conventions & Data Organisation Strategy
#----
## Param Set ID
1st col in CSV file of param sets is labeled 'ID'.
Each 'ID' is a number - a unique identifier ('ID') for that parameter set (row in CSV). It:
- forms part of filename for param file used to run a set of sims.
- is used to name dir in which data generated from sims using this param set will be stored.
This naming convention aids in effectively managing sims- helps identify/track param vals & corresponding results.

## `analysis_version` Var
label for current version of analysis - it:
- ensures ea version of analysis is stored separately, maintaining clear historical record of sims.
- used to make distinct dirs for ea version, preventing data overlap & ensuring clean, organised structure for storing sim data.
Manually update var if want to generate new CSV (eg w/ different params / param vals- for new version of analysis) / param files / sim data & don't want to overwrite old data.

## Replication of Sims
Ea set of sims using unique parameter set is executed/replicated multiple times.
'Replication' here refers to rerunning sim set w/ same param set.
It ensures results are robust & account for variability in sim outcomes.
For ea param set, we store data generated from ea replicate sim set in dedicated dir, nested within primary dir for that param set.
