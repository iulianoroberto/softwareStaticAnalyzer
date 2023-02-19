# Software Metrics Analyzer
Software Metrics Analyzer is a python base tool to evaluate the evolution of software quality in the years, on the base of metrics value, presence of clones and other factor of static analysis of source code. This tool takes advantage of the features provided by Nicad, Ck and Sonarqube.

## Features
The main features are:
- Filter the list of commits made to the repository by selecting a commit for each year of publication (the last of the year). This is necessary to determine the viewpoints of the analysis.
- Determine for each viewpoints:
  - Metrics value;
  - Number of clones;
  - Issue presence.
- Generate summary graphs of the data produced.

# Install Guide
Note that is is strongly recommended to use Ubuntu 22.04 or other Lubuntu version.

## Prerequisites

###### Nicad
[Nicad](https://www.txl.ca/txl-nicaddownload.html) is a flexible TXL-based hybrid language-sensitive / text comparison software clone detection system developed by James R. Cordy and Chanchal K. Roy, originally based on Chanchal's PhD thesis work. NiCad6 is a significantly new implementation with many important improvements and optimizations.

You need to install Nicad on main directory of the project. You Should creates a directory called "Nicad" on main directory of the project and put in its all files of Nicad installation.

For installation of Nicad see the guide on  website.

###### CK
[CK](https://github.com/mauricioaniche/ck) calculates class-level and method-level code metrics in Java projects by means of static analysis (i.e. no need for compiled code). Currently, it contains a large set of metrics, including the famous CK. 

You need to install CK on main directory of the project. You Should creates a directory called "CK_tools" on main directory of the project and put in its all files of CK installation (including jar file).

For installation of CK see the guide on  website.

###### Configuration
Insert in directory called "project_to_analize" the repository of software that you eant analyze. You can clone from GitHub the repositories that you want in this directory by "git clone" command.

###### Launch
Open the script by IDE, set the right paths in the code,  and launch "main.py" file.

# Preview
