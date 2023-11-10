# Text

### Indentation
Textwrap module can be used to format paragraphs
```python
import textwrap

sample_text = """
The textwrap module can be used to format text for output in situations where pretty-printing is desired. 
It offers programmatic functionality similar to the paragraph wrapping or filling features found in many text editors.
"""

# add indentation to the start of the string & sets width to 50 column
forty_space_filled = textwrap.fill(sample_text, width=40)
print(forty_space_filled)
# indentation for the first line be set different than the subsequent lines
custom_indentation = textwrap.fill(sample_text, width=50, initial_indent="", subsequent_indent="  " * 5)
print("\nCustom indentation: \n", custom_indentation)
# dedent can be used to un-indent the lines
dedent = textwrap.dedent(custom_indentation).strip()
print(f"Dented code:\n{dedent}")
# Note: Dedent only remove first level of space from all string
# indent can be used to add prefix to all lines
print(f"Indent example:\n{textwrap.indent(forty_space_filled, prefix='>>')}")
# A predicate can be passed to indent to conditionally add the prefix

def add_prefix(value):
    return len(value) % 2 ==0


print(f"Indent example:\n{textwrap.indent(forty_space_filled, prefix='>>', predicate=add_prefix)}")
```

### Truncation
`shorten` from `textwrap` can be used to convert existing whitespaces, newlines, tabs, multiple spaces to 
standard single space.

```python
print(textwrap.shorten(sample_text, width=80))
# default placehoder is [...], but it can be changed
print(textwrap.shorten(sample_text, width=80, placeholder=" ...PTO"))
```