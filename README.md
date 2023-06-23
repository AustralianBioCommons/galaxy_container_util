galaxy_container_util
==============
Implements the "container avail" utility for searching images published on the singularity.galaxyproject.org CVMFS 
repository.

# Usage instructions for using "container avail" utility
The ```container``` utility should be considered a working prototype.

Python 3.X needs to be installed on the target system. The script has been tested with versions 3.6 - 3.10 in RHEL,
Ubuntu, Windows and MacOS. The container script uses only the standard libraries.

The Python script ```container``` in this repository should be copied into /usr/local/sbin or similar script directory 
included in the user's PATH environment variable, and executable permissions set using 
```chmod 755 /usr/local/sbin/container```.

If the /cvmfs/singularity.galaxyproject.org directory is not present on the target system, then the ```container``` 
utility will download a file listing from the AARNet UAT stratum 1 CVMFS service. This publicly-accessible list file 
is refreshed every 30 minutes using the script ```update_repo_list.sh``` on the stratum 1 server.

```
$ container --help
usage: container [-h] [-q] [-r] [-a | -l] [-m | -s] [-v VERSION] [arguments [arguments ...]]

container v0.0.1 - "container avail" helps you locate and access thousands of container images available via a read-only 
filesystem (CERN VM-FS). This service is currently available at the NCI and Pawsey Australian Compute Facilities

positional arguments:
  arguments             <command (avail)> <tool name search string(s) (use * for wildcard - must be quoted for *nix)>

optional arguments:
  -h, --help            show this help message and exit
  -q, --quiet           Suppress optional output and show only image paths
  -r, --refresh         Force cache refresh
  -a, --all             Show ALL images for each tool
  -l, --latest          Show only latest image by version and build, or by date modified if --modified flag used
  -m, --modified        Sort by ascending file modification datetime instead of version and build (DANGEROUS!)
  -s, --size            Sort by ascending file size instead of version and build
  -v VERSION, --version VERSION
                        Filter images by version
```
For example:

- ```container avail samtools``` will list all image information available for the most recent version of "samtools" (with ALL optional information)
- ```container avail samtools -q``` will list all image paths available for the most recent version of "samtools" (with NO optional information)
- ```container avail samtools -ql``` will list the latest image path available for the most recent version of "samtools" (with NO optional information)
- ```container avail samtools -qv 1.2``` will list all image paths available for "samtools" version 1.2 (with NO optional information)
- ```container avail '*rna*' -ql``` will list the latest image paths available for all tools containing the string 'rna' (with NO optional information). 
Note that the '*' wildcard character should be quoted to avoid evaluation in the shell.
- ```container avail``` will list all images available for the most recent version of every tool (with ALL optional information) - LONG!

---

# Attributions

The initial version of the container utility was written by Alex Ip of AARNet Pty. Ltd. [@alex-ip](https://github.com/alex-ip)

The guideline documentation template is supported by the Australian BioCommons via Bioplatforms Australia funding, the 
Australian Research Data Commons (https://doi.org/10.47486/PL105) and the Queensland Government RICF programme. 
Bioplatforms Australia and the Australian Research Data Commons are enabled by the National Collaborative 
Research Infrastructure Strategy (NCRIS).

The BioCommons would also like to acknowledge the contributions of the following individuals and institutions to these 
documentation guidelines:

- Johan Gustafsson (Australian BioCommons, University of Melbourne) [@supernord](https://github.com/supernord)
- Brian Davis (National Computational Infrastructure) [@Davisclan](https://github.com/Davisclan)
- Marco de la Pierre (Pawsey Supercomputing Centre) [@marcodelapierre](https://github.com/marcodelapierre)
- Audrey Stott (Pawsey Supercomputing Centre) [@audreystott](https://github.com/audreystott)
- Sarah Beecroft (Pawsey Supercomputing Centre) [@SarahBeecroft](https://github.com/SarahBeecroft)
- Matthew Downton (National Computational Infrastructure) [@mattdton](https://github.com/mattdton)
- Richard Edwards (University of New South Wales) [@cabbagesofdoom](https://github.com/cabbagesofdoom)
- Tracy Chew (University of Sydney) [@tracychew](https://github.com/tracychew)
- Georgina Samaha (University of Sydney) [@georgiesamaha](https://github.com/georgiesamaha)



