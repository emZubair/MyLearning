
## Regular Expressions
Regular expressions can be used to search for words or patterns in strings.
The `search` function is used to search group matching given pattern, if match is found, it returns a `Match` object 
is returned, otherwise a None value is returned.

```python
from re import search, compile

pattern = "lazy"
msg = "A quick brown fox jumps over the lazy dog."
match = search(pattern, msg)
print(f"Word {msg[match.start():match.end()]!r} found, by pattern {match.re.pattern!r} inside {match.string!r}")
# compile can be used to compile frequently used expressions 
regexes = [compile(pattern) for pattern in ["dog", "fox", "active"]]
for regex in regexes:
    print(f"Seeking, {regex.re.pattern}", end="")
    if regex.search(msg):
        print("Found")
    else:
        print("Not found")
```
`findall` function returns all of the substrings of the input that match the pattern without overlapping.
`finditer` can be used to get all `Match` objects instead of strings as opposed to `findall`
```python
import re
msg = "A quick brown fox jumps over the lazy dog. A quick brown fox jumps over the lazy dog."
pattern = 'dog'
for match in re.findall(pattern, msg):
    print('Found {!r}'.format(match))

for match in re.finditer(pattern, msg):
    start = match.start()
    end = match.end()
    print(f"start index {start=} {end=}, matched str is :'{msg[start:end]}'")
```

## Repetition
There are 5 ways to express repetition in a pattern.
1. A pattern followed by `*`, is repeated by zero or more times, will match even if it doesn't appear 
2. `+` means, the pattern must appear at least once.
3. `?` means pattern appears zero or one time.
4. Use `{m}` after the pattern for `m` number of repetitions. 
5. Use `{m,n}` after pattern to allow minimum `m` and maximum `n` repetitions, use `{m, }` to match minimum `m` patterns 
with no maximum limit.

```python
import re

def find_patterns(string, patterns):
    for pattern, detail in patterns:
        print(f"{pattern=}, {detail=}\n\n'{string}'")
        for match in re.finditer(pattern, string):
            start = match.start()
            end = match.end()
            matched = string[start:end]
            back_slashes = string[:start].count("\\")
            prefix = "." * (start + back_slashes)
            print(f"{prefix}'{matched}'")
        print()

# greedy instruction
find_patterns('abbaabbba', [
    ('ab*', 'a followed by zero or more b'),
    ('ab+', 'a followed by one or more b'),
    ('ab?', 'a followed by zero or one b'),
    ('ab{3}', 'a followed by three b'),
    ('ab{2,3}', 'a followed by two to three b')
])
# Non greedy instruction 
find_patterns('abbaabbba', [
    ('ab*?', 'a followed by zero or more b'),
    ('ab+?', 'a followed by one or more b'),
    ('ab??', 'a followed by zero or one b'),
    ('ab{3}?', 'a followed by three b'),
    ('ab{2,3}?', 'a followed by two to three b')
])
```
By default the pattern matching tries to match as much as possible, known as greedy behaviour, which can be turned off by 
placing `?` after the repetition instruction.

### Character Set
Is a set of characters which can match i.e. [xy] will match either `x` or `y`
```python
find_patterns('xyyxxyyyx', [
    ('[xy]', 'either x or y'),
    ('x[xy]+', 'x followed by one or more x or y'),
    ('x[xy]+?', 'x followed by one or more x or y (greedy turned off)'),
    ('x[xy]*', 'x followed by zero or more x or y'),
    ('x[xy]*?', 'x followed by zero or more x or y'),
])
```
`Character ranges` are used to specify the range between the start & endpoint of the range.
```python
find_patterns('A quick brown --- fox, jumps over. the Lazy DOg.', [
    ('[a-z]+', 'lower cased range'),
    ('[A-Z]+', 'Upper cased range'),
    ('[a-zA-Z]+', 'lower and upper cased range'),
    ('[A-Z][a-z]+', 'One upper case followed by lower case'),
])
```

`Negation` The carat `(^)` symbol is used to look for the characters that don't match the set following the carat symbol. 

```python
find_patterns('A quick brown --- fox, jumps over. the Lazy D.O.G.', [
    ('[^-. ]', 'A sequence without `-, . and space`'),
    ('[^-. ]+', 'A sequence without `-. . and space`'),
    ('[^-. ]+?', 'A sequence without `-. . and space`'),
])
```

`meta character` dot `(`)` specifies that the pattern should match any single character in that position.
```python
```python
find_patterns('abbaabbba', [
    ('a.', 'a followed by any one character'),
    ('b.', 'b followed by any one character'),
    ('a.*b', 'a followed by anything, ending with b'),
    ('a.*?b', 'a followed by anything, ending with b'),
])
```
`Escape Codes` & `Anchors` can be used to represent predefined character sets.

|  Code  | Meaning (Pattern)                     | Code  | Meaning (Anchor)                                            |
|:------:|:--------------------------------------|:-----:|:------------------------------------------------------------|
|   \d   | A digit                               |   ^   | Start of string or line                                     |
|   \D   | A non digit                           |   $   | End of string or line                                       |
|   \s   | Whitespace (tab, space, newline etc.) |  \A   | Start of String                                             |
|   \S   | Non-whitespace                        |  \Z   | End of String                                               |
|   \w   | Alphanumeric                          |  \b   | Empty string at the beginning or at the end of the word     |
|   \W   | Non-alphanumeric                      |  \B   | Empty string not at the beginning or at the end of the word |
```python
find_patterns('A quick brown fox, jumps over #3 lazy dogs.!', [
    ('\d+', 'Sequence of digits'),
    ('\D+', 'Sequence of non-digits'),
    ('\s+', 'Sequence of whitespaces'),
    ('\S+', 'Sequence of non-whitespaces'),
    ('\w+', 'Sequence of alphanumeric'),
    ('\W+', 'Sequence of non-alphanumeric'),
])
```
In order to escape special characters, use escape characters
```python
find_patterns('\d+ \S+ \s+ \DS+', [
    ('\\.\+', 'escape code'),
    (r'\\.\+', 'escape code'),
])
```

### Anchoring
Relative location can be specified in the input text where the pattern should appear using anchoring.
```python
find_patterns(
    'This is some text -- with punctuation.',
    [(r'^\w+', 'word at start of string'),
     (r'\A\w+', 'word at start of string'),
     (r'\w+\S*$', 'word near end of string'),
     (r'\w+\S*\Z', 'word near end of string'),
     (r'\w*t\w*', 'word containing t'),
     (r'\bt\w+', 't at start of word'),
     (r'\w+t\b', 't at end of word'),
     (r'\Bt\B', 't, not start or end of word')],
)
```