## About
As a recruiter, it is tedious to manually read through transcripts to figure out whether a candidate has taken a particular class and how well they performed in the class. 
This tool automatically parses a folder with University of Michigan transcripts and highlights their grade (if they took the course) in the course of interest, which is specified in a config file. 


## Setup
- Store all of the transcripts in a folder
  - Must be PDFs
  - Default is ```{directory with ATS-transcript.exe}/data/input/transcript/```
- Write the config file 
  - Ensure there is a header for the column of course names (see data/input/config.csv)
  - Default is ```{directory with ATS-transcript.exe}/data/input/config.csv```
- Choose an output directory
  - Default is ```{directory with ATS-transcript.exe}/data/output/```

## Usage
Download and run the executable (ATS-transcript.exe)


## Prerequisites
(Tool is run on Windows? Not tested on MacOS)


<!-- ROADMAP -->
## Roadmap

- [x] Finish V1.0
- [ ] Write developer notes in README
- [ ] Enhance UI and output file
- [ ] Test on MacOS


## Contact

Anan Nuengchana - ananueng@umich.edu
