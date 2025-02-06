# MCON-532-Sprint-2025
### Welcome to MCON-532! This repository will be used to publish assignements and demos.
All students need to :
- Create a fork for this repo
- Clone your fork
- Set your fork as origin and this repo as upstream
Execrcises will be added to this repo so you will need to do periodic pulls from this repo to get the updates and merge the changes.
This will allow you to practice working with Git as well

### Content of the repo
## Anagram grouping 
- Create a function that takes a list of strings and groups anagrams together.
- Anagrams are words that have the same characters but in different order.
- Example: ['eat', 'tea', 'tan', 'ate', 'nat', 'bat'] => [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
- The function should return a list of lists of strings.   

### Explanation
```python
for word in words:
    key = ''.join(sorted(word))
    anagrams.setdefault(key, []).append(word)
```
For each word, we generate a key by sorting the characters of the word using sorted(word).
Sorting ensures that all anagrams produce the same key because they have the same characters.
Example:

"listen" -> ['e', 'i', 'l', 'n', 's', 't'] -> "eilnst"
"silent" -> ['e', 'i', 'l', 'n', 's', 't'] -> "eilnst"
Step 2: Group Words by Anagram Signature
setdefault(key, []).append(word) does two things:
If key does not exist in the dictionary, it initializes it with an empty list.
Appends the current word to the corresponding list.
Example Execution
Iteration 1 (word = "listen"): {"eilnst": ["listen"]}
Iteration 2 (word = "silent"): {"eilnst": ["listen", "silent"]}
Iteration 3 (word = "rat"): {"eilnst": ["listen", "silent"], "art": ["rat"]}
Iteration 4 (word = "tar"): {"eilnst": ["listen", "silent"], "art": ["rat", "tar"]}

