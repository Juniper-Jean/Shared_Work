#!/usr/bin/python

"""	Examples of regular expressions - a tool to find patterns in strings.
		Shows the use of the 're.search' function."""

__author__ = 'Calum Pennington (c.pennington@imperial.ac.uk)'
__version__ = '0.0.1'

import re
# Import the module with regex functions.

my_string = "a given string"
match = re.search(r'\s', my_string) # Find a space in the string
# 're.search' searches a string and finds the first match of the given pattern.
# 'r' in front of the regex passes the pattern as a raw string - tells Python to read it literally.
# This is customary as the pattern may include special characters, e.g. Python uses backslash '\'as an escape sequence.

print match
# This should print something like
# <_sre.SRE_Match object at 0x93ecdd30>
# Matches are stored in RAM memory - this is the "address".

# now we can see what has matched
match.group()
# '.group()' returns the match.

match = re.search(r's\w*', my_string)
# Find 's', followed by 0 or more alphanumeric characters.

match.group()
# Returns 'string'.


## NOW AN EXAMPLE OF NO MATCH:
match = re.search(r'\d', my_string)
# Find a digit.

print match
# Prints 'None'.


## Further Example
my_string = 'an example'
match = re.search(r'\w*\s', my_string)
# Find 0 or more alphanumeric characters, followed by a space.
# Finds 'an '. See 'match.group()'.

if match:
	print 'found a match:', match.group()
else:
	print 'did not find a match'
# Prints a different message, depending on if a match was found. Prints matches.


## More Basic Examples
match = re.search(r'\d' , "it takes 2 to tango")
print match.group()
# Find a numeric character.
# Prints '2'.

match = re.search(r'\s\w*\s', 'once upon a time')
match.group()
# Find 0 or more alphanumeric characters, preceded and followed by a space.
# Finds ' upon '.

match = re.search(r'\s\w{1,3}\s', 'once upon a time')
match.group()
# Find 1-3 alphanumeric characters, preceded and followed by a space.
# Finds ' a '.

match = re.search(r'\s\w*$', 'once upon a time')
match.group()
# Find 0 or more alphanumeric characters that are at the end of the line ('$') and preceded by a space.
# Finds ' time'.

match = re.search(r'\w*\s\d.*\d', 'take 2 grams of H2O')
match.group()
# Find 0 or more alphanumeric characters, followed by a space, then a digit, any ('.') and all ('*') characters, and a digit.
# Finds 'take 2 grams of H2'.

match = re.search(r'^\w*.*\s', 'once upon a time')
match.group()
# At the start of a line ('^'), find 0 or more alphanumeric characters, followed by any and all characters (except line break), and a space.
# Finds 'once upon a '.


## NOTE
## *, +, and { } are all "greedy":
## They repeat the previous regex token as many times as possible.
## As a result, they may match more text than you want.

## To make it non-greedy, use ?:
match = re.search(r'^\w*.*?\s', 'once upon a time')
match.group()
# At the start of a line, find 0 or more alphanumeric characters, followed by any character and a space.
# Seems to return the same as '^\w*.\s' - '?' cancels out the greedy '*'.
# Finds 'once '.

## To further illustrate greediness, let's try matching an HTML tag:
match = re.search(r'<.+>', 'This is a <EM>first</EM> test')
match.group()
# Find '<', followed by any character 1 or more times, and '>'.
# Finds '<EM>first</EM>'.

## But we didn't want this: we wanted just <EM>
## It's because + is greedy!
## Instead, we can make + "lazy"!
match = re.search(r'<.+?>', 'This is a <EM>first</EM> test')
match.group() # '<EM>'
# '?' - match the preceding element 0 or 1 times.
# '+' - 1 or more times
# Thus, '.+?' means find a string of any 2 characters.
# Here, you need to both '+' and '?'. '+' instructs Python to match '.' 1 or more times, and '?' to limit this to just 1 time.


## OK, moving on from greed and laziness
match = re.search(r'\d*\.?\d*','1432.75+60.22i') # Note '\' before '.'
match.group() # '1432.75'
match = re.search(r'\d*\.?\d*','1432+60.22i')
match.group() # '1432'
# Find 0 or more digits. Find them whether or not they're separated by a dot.
# Finds the number before '+'.

match = re.search(r'[AGTC]+', 'the sequence ATTCGT')
match.group()
# Find upper case a, t, g or c (any of them) 1 or more times.
# Finds 'ATTCGT' - extracts the sequence of DNA bases from the string.

## NOTE THAT I DIRECTLY RETURN THE RESULT BY APPENDING .group()
re.search(r'\s+[A-Z]{1}\w+\s\w+', 'The bird-shit frog''s name is Theloderma asper').group()
# Find 0 or more spaces, followed by one upper case letter, then 1 or more alphanumeric characters, a space, and 1 or more alphanumeric characters.
# Finds ' Theloderma asper' - extracts the latin species name from the string.
# Note 2 inverted commas so as not to close the string early.
