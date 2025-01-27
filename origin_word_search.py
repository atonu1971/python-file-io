#! /usr/bin/env python3
#This script is made to search all words related to any specific term from a specific txt file. Final file inherit-times.txt will contain the result.

import sys
import re

def find_iter(in_stream, target_regex,
        start_regex = None,
        stop_regex = None):
        
        """
    Parameters
    ----------
    in_stream : File object or string. Input stream for 'target_regex'.
    target_regex: Regex object. Target pattern found in `in_stream`.
    start_regex : Rgex object or none
    stop_regex : Regex object or none
    Pattern be matcher in  `in_stream` before `target_regex` search starts. target regex searching will start after the start regex line matched. If there is
    none search begins at the first line. 
   
    """
   
    search_has_started = False
    if not start_regex:
        search_has_started = True
    for line_index, line in enumerate(in_stream):
        if stop_regex and stop_regex.match(line):
            break
        if start_regex and (not search_has_started):
            if start_regex.match(line):
                search_has_started = True
            continue
        for match_object in target_regex.finditer(line):
            yield line_index, match_object

def record_all_occurrences(in_stream, out_stream,
        target_regex,
        start_regex = None,
        stop_regex = None):
        
         """
      Search all occurences of regex pattern in `target_regex` in `in_stream`, and output the numbers of lines with string `out_stream`
    '\t' character separates the number and string. 
    
    Parameters
    ----------
    in_stream : File object or string. Input stream for 'target_regex'.
    target_regex: Regex object. Target pattern found in `in_stream`.
    start_regex : Rgex object or none
    stop_regex : Regex object or none
    Pattern be matcher in  `in_stream` before `target_regex` search starts. target regex searching will start after the start regex line matched. If there is
    none search begins at the first line. 
   
    Returns
    -------
    int
        The number of `target_regex` occurences was matched in `in_stream`.
    """
  
    num_occurrences = 0
    for line_index, match_obj in find_iter(in_stream, target_regex,
            start_regex, stop_regex):
        num_occurrences += 1
        for target_str in match_obj.groups():
            out_stream.write("{line_num}\t{string}\n".format(
                    line_num = line_index + 1,
                    string = target_str))
    return num_occurrences

if __name__ == '__main__':
    target_pattern = re.compile(r'(\w*herit\w*)', re.IGNORECASE)
    start_pattern = re.compile(r'^\*\*\*\s*START.*$')
    stop_pattern = re.compile(r'^\*\*\*\s*END.*$')
    in_path = "origin.txt"
    out_path = "inherit-times.txt"
    with open(in_path, 'r') as in_stream:
        with open(out_path, 'w') as out_stream:
            num_occurrences = record_all_occurrences(in_stream = in_stream,
                    out_stream = out_stream,
                    target_regex = target_pattern,
                    start_regex = start_pattern,
                    stop_regex = stop_pattern)
    message = "Darwin referred to heritability {0} times in origin of species!".format(
            num_occurrences)
    print(message)
