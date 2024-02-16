#!/bin/bash

texcount -incbib -1 -sum Report.tex > Report_Word_Count.txt
echo `head -2 Report_Word_Count.txt` > Report_Word_Count.txt
