#!/usr/bin/env python

import json
import sys

j = json.load(sys.stdin)

q = sys.argv[1]

ppath = False
if sys.argv[2] == '-p':
  ppath = True


def traverse(data,stack, path):
  if len(stack) == 0:
    if ppath:
      print ".".join(path),
    print json.dumps(data)
  elif stack[0] == '*':
    for elem in data.keys():
      np = path[:]
      np.append(elem)
      traverse(data[elem], stack[1:], np)
  elif stack[0].startswith('[') and stack[0].endswith(']'):
    if isinstance(data, list):
      slicer = stack[0][1:-1].split(':')
      if len(slicer) == 1:
        idx = int(slicer[0])
        np = path[:]
        np.append(str(idx))
        traverse(data[idx], stack[1:], np)
      if len(slicer) == 2:
        start = slicer[0]
        end   = slicer[1]
        if start == "":
          start = 0
        else:
          start = int(start)
        if end == "":
          end = len(data)
        else:
          end = int(end)
        if start < 0:
          start = len(data) + start
        if end < 0:
          end = len(data) + end
        sliced = data[start:end]
        for offset,elem in enumerate(sliced):
          idx = start + offset
          np = path[:]
          np.append(str(idx))
          traverse(data[idx], stack[1:], np)
    if isinstance(data, dict):
      for elem in data.keys():
        if stack[0][1:-1] in elem:
          np = path[:]
          np.append(elem)
          traverse(data[elem], stack[1:], np)
  else:
    if isinstance(data, dict):
      if stack[0] in data.keys():
        np = path[:]
        np.append(stack[0])
        traverse(data[stack[0]], stack[1:], np)

def tokenize(q):
  tokens = []
  current_word = ""
  in_regex = False
  sq_bracket_nest = 0
  array_token = False
  for c in q:
    if c == '.' and not in_regex:
      tokens.append(current_word)
      current_word = ""
    elif c == '[' and not in_regex and current_word == "":
      in_regex = True
      current_word += c
    elif c == '[' and not in_regex:
      array_token = True
      tokens.append(current_word)
      current_word = c
    elif c == '[' and in_regex:
      sq_bracket_nest += 1
      current_word += c
    elif c == ']' and in_regex and sq_bracket_nest == 0:
      in_regex = False
      current_word += c
    elif c == ']' and in_regex:
      sq_bracket_nest -= 1
      current_word += c
    elif c == ']' and array_token:
      current_word += c
    else:
      current_word += c

  tokens.append(current_word)
  if tokens[0] == "":
    tokens = tokens[1:]
  return tokens

print >> sys.stderr, "query:",
print >> sys.stderr, tokenize(q)

traverse(j,tokenize(q), [])

