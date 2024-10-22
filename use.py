# from codebleu import calc_codebleu

# prediction = "public function add(a,b) { return (a+b) }"
# reference = "public function sum(a,b) { return (a+b) }"

# result = calc_codebleu([reference], [prediction], lang="java", weights=(0.25, 0.25, 0.25, 0.25), tokenizer=None)
# print(result)

# from codebleu import calc_codebleu

# prediction = "def add ( a , b ) :\n return a + b"
# reference = "def sum ( first , second ) :\n return second + first"

# result = calc_codebleu([reference], [prediction], lang="python", weights=(0.25, 0.25, 0.25, 0.25), tokenizer=None)
# print(result)

from codebleu import calc_codebleu

prediction = """function foo(x)
  real :: foo
  foo = x
end function foo
"""
reference = """function foo(x)
  real :: foo
  foo = x
end function foo
"""

result = calc_codebleu([reference], [prediction], lang="fortran", weights=(0.25, 0.25, 0.25, 0.25), tokenizer=None)
print(result)
