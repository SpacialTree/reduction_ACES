"""
Run this with some care; it will require manual pushing

Example call:
ACES_ROOTDIR=/orange/adamginsburg/ACES/reduction_ACES/ python ${ACES_ROOTDIR}/pipeline_scripts/generate_spw33_commands.py
"""

import json, os, sys

if os.getenv('ACES_ROOTDIR') is None:
    raise ValueError("Specify ACES_ROOTDIR environment variable ")
else:
    rootdir = os.environ['ACES_ROOTDIR']
    sys.path.append(rootdir)
    sys.path.append(f'{rootdir}/pipeline_scripts')

from merge_tclean_commands import commands

with open(f"{rootdir}/pipeline_scripts/default_tclean_commands.json", "r") as fh:
    default_commands = json.load(fh)

with open(f"{rootdir}/pipeline_scripts/override_tclean_commands.json", "r") as fh:
    override_commands = json.load(fh)
ncmds = (len(override_commands))


chwid = '488244Hz'
nchan = 3836
start = "97.6660537907GHz"

for key in commands:
    if 'TM' in key:
        if 'spw33' not in commands[key]['tclean_cube_pars']:
            print(f"Adding {key}")
            spw33pars = commands[key]['tclean_cube_pars']['spw35']
            spw33pars['imagename'] = spw33pars['imagename'].replace('35', '33')
            spw33pars['nchan'] = nchan
            spw33pars['start'] = start
            spw33pars['width'] = chwid
            spw33pars['threshold'] = '0.01Jy'
            spw33pars['spw'] = [x.replace('35','33') for x in spw33pars['spw']]
            if key in override_commands:
                override_commands[key]['tclean_cube_pars']['spw33'] = spw33pars
            else:
                override_commands[key] = {'tclean_cube_pars': {'spw33': spw33pars}}
        elif commands[key]['tclean_cube_pars']['spw33']['nchan'] < 3800:
            print(f"Modifying {key}")
            spw33pars = {}
            spw33pars['nchan'] = nchan
            spw33pars['start'] = start
            spw33pars['width'] = chwid
            spw33pars['threshold'] = '0.01Jy'
            if key in override_commands:
                override_commands[key]['tclean_cube_pars']['spw33'] = spw33pars
            else:
                override_commands[key] = {'tclean_cube_pars': {'spw33': spw33pars}}

assert len(override_commands) >= ncmds

with open(f"{rootdir}/pipeline_scripts/override_tclean_commands.json", "w") as fh:
    json.dump(override_commands, fh, indent=2)
