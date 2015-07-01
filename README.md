JSQuery
=======

A command-line tool for querying json.

Background
----------

I've not been able to find a tool that really meets my needs as far as inspecting json goes.

I've used jq and jsawk, and they are useful for many things, but there are two big problems with them:

1. It is awkward (jq) or impossible (jsawk) to traverse the structure based on key matches
2. You can't get the path back that matched the query

So, I've banged out a small script to to allow me to do these things. It's very much a work in progress.

Usage
-----

    $ echo '{"path": {"to": {"traverse": {"str": "asdf", "int": 1}, "other": ["a","b",{"c": 1}]}}}' > some.json

    $ cat some.json | jsquery 'path.to.traverse' -p
    path.to.traverse {"int": 1, "str": "asdf"}

    # * to match all keys
    $ cat some.json | jsquery 'path.to.traverse.*' -p
    path.to.traverse.int 1
    path.to.traverse.str "asdf"

    # substring match on keys
    $ cat some.json | jsquery 'path.to.[ave].*' -p
    path.to.traverse.int 1
    path.to.traverse.str "asdf"

    # array indexing
    $ cat some.json | jsquery 'path.to.other[1]' -p
    path.to.other.1 "b"
    
    # array slicing
    $ cat some.json | jsquery 'path.to.other[:-1]' -p
    path.to.other.0 "a"
    path.to.other.1 "b"

    # array slicing
    $ cat some.json | jsquery 'path.to.other[:]' -p
    path.to.other.0 "a"
    path.to.other.1 "b"
    path.to.other.2 {"c": 1}

    # pruning unmatched paths
    $ cat some.json | jsquery 'path.to.other[:].c' -p
    path.to.other.2.c 1

Just use dot-path notation to traverse map keys. Using `*` as a key will match any key, and surrounding the key with brackets (`[]`) will do a substring match.

To traverse arrays, use array indexing or slicing.

JSQuery should prune any paths that don't match (as in the last example).

If you just want to get the values back without the keys, use '-np' instead of '-p'.

Wish List
---------

* use regex instead of substring match for `[key]`
* add argparse instead of indexing into `sys.argv`
* add value matchers
* consider: add json manipulation?

