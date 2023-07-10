[tool / workflow name] on [system name] @ [infrastructure name]
===========

---

# Accessing tool/workflow

```
This tool needs to be installed manually.
```

---

# Installation

```
The container script needs to be copied into a script directory in your search path (e.g. /usr/local/sbin) and 
execute permissions assigned to it.
```

---

# Quickstart tutorial

```
usage: container [-h] [-q] [-r] [-a | -l] [-m | -s] [-v VERSION]
                 [arguments ...]

container v0.0.2 - "container avail" helps you locate and access thousands of
container images available via a read-only filesystem (CERN VM-FS). This
service is currently available at the NCI and Pawsey Australian Compute
Facilities

positional arguments:
  arguments             <command (avail)> <tool name search string(s) (use *
                        for wildcard - must be quoted for *nix)>

options:
  -h, --help            show this help message and exit
  -q, --quiet           Suppress optional output and show only image paths
  -r, --refresh         Force cache refresh
  -a, --all             Show ALL images for each tool
  -l, --latest          Show only latest image by version and build, or by
                        date modified if --modified flag used
  -m, --modified        Sort by ascending file modification datetime instead
                        of version and build (DANGEROUS!)
  -s, --size            Sort by ascending file size instead of version and
                        build
  -v VERSION, --version VERSION
                        Filter images by version
```

---

# Optimisation required

```
Were any optimisations required that were specific to the HPC / HTC infrastructure used?
```

---

# Acknowledgements / citations / credits

```
Any attribution information that is relevant to the workflow being documented, or the infrastructure being used.
```

---
