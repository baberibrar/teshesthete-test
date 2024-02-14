def longest_palindrome(s: str) -> str:
    if not s:
        return ""

    n = len(s)
    dp = [[False] * n for _ in range(n)]
    start = 0
    max_len = 1

    # Every single character is a palindrome of length 1
    for i in range(n):
        dp[i][i] = True

    # Check for palindromes of length 2
    for i in range(n - 1):
        if s[i] == s[i + 1]:
            dp[i][i + 1] = True
            start = i
            max_len = 2

    # Check for palindromes of length > 2
    for length in range(3, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j] and dp[i + 1][j - 1]:
                dp[i][j] = True
                if length > max_len:
                    start = i
                    max_len = length

    return s[start:start + max_len]

# Example usage:
s1 = "babad"
s2 = "cbbd"
print(longest_palindrome(s1))  # Output: "bab" or "aba"
print(longest_palindrome(s2))  # Output: "bb"
