# Morphological analyzers and finite-state transducers


## 1. [`analyzer.fst`](analyzer.fst): Morphology of English nouns

This is a simple FST for a small group of English nouns.

The code works with `hfst-xfst` from
[HFST](https://hfst.github.io/).

Example of interactive session with `hfst-xfst`
:

```
$ hfst-xfst
hfst[0]: source analyzer.xfst
hfst[1]: down cat<N><SG>
cat
hfst[1]: up cats
cat<N><PL>
hfst[1]: up
apply up> foxes
fox<N><PL>
apply up> foxs
???
```

In analysis mode, the system is presented with a word's surface form
and provide an analysis, e.g., given _cats_  get
`cat<N><PL>`.
Generation is the reverse mode.

The underlying forms (analyses) are the input language,
and surface forms (actual words) are the output language.
By default the transducer generates surface forms
from the underlying representations.
To use it as an analyzer,
the transducer needs to be inverted.

In the XFST,
`apply down` means transduce from the input language to the output language(morphological generator).
`apply up` means transduce from the output language to the input language(morphological analyzer).

In the first example above,
the transducer generates _cat_ from the analysis string `cat<N><SG>`.
The otheranalysis examples,
where _cats_ and _foxes_are correctly analyzed,
while incorrect forms _*cates_ and _*foxs_ are rejected

The resulting finite state transducer is saved as `analyzer.fst` in AT&T format.


## 2. [`fst.py`](fst.py): Finite-state transducer

This is a simple FST in python.


### 1. Read an ATT transducer file

FST is created by reading in AT&T format files.

This is an example of a transducer that accepts at least one
`a`, all input will be replaced by `b`, and the final `a` will
be replaced by empty string(deleted).
Note: `@0@` means an empty string, ε.

```
0       1       a       @0@
0       0       a       b
1
```

The format have four columns,
_source state_, _target state_, _input symbol_, and _output symbol_,
separated by tabs.

The `read_att()` method reads in such a file,
and creates the FST transition table.

### 2. The transduction

The `transduce()` method returns the list of
output strings for a given accepted input.

Epsilon transitions are handled during
transduction(recognition).

Multi-character symbols, such as `<N>` on FST transitions.
This `transduce()` method tokenizes
the input string with the multi-char symbols correctly.

### 3. Inversion

The `invert()` method that inverts the FST in-place.

Input and outputs symbols on all transitions are swapped.

### 4. Command line interface

The command line interface:

- `python3 fst.py analyze fst_file input_file` read in the
    AT&T-formatted `fst_file`, and produces morphological analyses
    for all words in the `input_file`.
    Input file should contain one word per line.
    The output will list all analyses of a word on single row.
    For example, for the `analyzer.fst` and a input file
```
cats
fish
```
the output should be

```
cat<N><PL>
fish<N><SG> fish<N><PL>
```
- `python3 fst.py generate fst_file input_file` reads in the
    `fst_file` and produce all outputs for the words in the `input_file`.
    Input and output formats should be the same as `analyze` above.

