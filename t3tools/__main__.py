#!/usr/bin/env python
# encoding: utf-8
# Victor Amin 2013

import sys
import os
import argparse

sys.path.append(os.path.join(os.path.dirname( __file__ ), '..' )) # add parent
                                                                  # dir to path
from _tools import ToolsManager
from _import import T3

def main():
    toolsmanager = ToolsManager()
    
    parser = argparse.ArgumentParser(
	    description="A collection of tools to parse and analyze T3 data.",
	    formatter_class=argparse.ArgumentDefaultsHelpFormatter)#,
	    #add_help=False)
    
    toolsmanager.populate_parser(parser) # loads tool-specific arguments

    # run tool with args
    args = parser.parse_args()
    tool = toolsmanager.load_tool(args.subparser_name)
#    t3 = T3(args.T3)
#    exit()
    tool.load(T3(args.T3))
    tool.execute(args)

if __name__ == '__main__':
    main()
