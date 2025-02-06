def group_anagrams(words: list[str]) -> dict[str, list[str]]:
    """
    Groups anagrams from the given list of words.

    Args:
        words (list[str]): List of input words.

    Returns:
        dict[str, list[str]]: Dictionary grouping words by their anagram signature.
    """
    anagrams = {}

    for word in words:
        # Sort the word's characters to create a signature for anagrams
        key = ''.join(sorted(word))
        anagrams.setdefault(key, []).append(word)

    return anagrams


def main():
    words = ['listen', 'silent', 'enlist', 'hello', 'world', 'cat', 'act']
    result = group_anagrams(words)

    for key, anagrams in result.items():
        print(f'{key}: {anagrams}')


if __name__ == '__main__':
    main()
