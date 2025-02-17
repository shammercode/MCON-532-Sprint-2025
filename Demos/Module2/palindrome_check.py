def is_palindrome(s: str) -> bool:
    """
    This method receives a string and returns a bool of whether
    it is a palindrome. It ignores case sensitivity, spaces, and
    non alpa-numeric characters.
    Parameters:
        s: str
            string tested for palindrome
    Returns:
        bool
            True if s is a palindrome, False if not
    """
    forward_list = []
    stack = []
    s=s.lower()
    for i in s:
        if i.isalpha():
            forward_list.append(i)
            stack.append(i)
    for i in forward_list:
        if i != stack.pop():
            return False
    return True


def main():
    input_str = input("Enter a phrase to see of it's a palindrome: ")
    print(input_str+ "is a palindrome: " + str(is_palindrome(input_str)))


if __name__ == '__main__':
    main()
