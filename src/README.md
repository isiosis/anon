# resume-anonymizer

It applies the find-and-replace rules laid out in `rules.json` (or what you specify in `-r`) to the files specified in its command-line arguments (which may be any sort of text file; specify in `-i`), writing the result to files with the same name, but `anonymized_` in front.

Sample usage:
``` 
> python anonymize.py -i resume.tex res2you.tex
rules applied; result written to anonymized_resume.tex
rules applied; result written to anonymized_res2you.tex
```

Sample `rules.json`:
```
[
  {"Sarah Lawrence College" : "Liberal Arts College"},
  {"Uniqua Speziale" : "John Doe"},
  {"uniqua@speziale.com" : "first@lastname.com"},
  {"Shiny Watches inc." : "Generic Widgets inc."}
]
```

## testing

``` pytest ```
