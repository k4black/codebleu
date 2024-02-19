from codebleu import calc_codebleu

#prediction = "def add ( a , b ) :\n return a + b"
#reference = "def sum ( first , second ) :\n return second + first"
#result = calc_codebleu([reference], [prediction], lang="python", weights=(0.25, 0.25, 0.25, 0.25), tokenizer=None)
#print(result)

# {
#   'codebleu': 0.5537, 
#   'ngram_match_score': 0.1041, 
#   'weighted_ngram_match_score': 0.1109, 
#   'syntax_match_score': 1.0, 
#   'dataflow_match_score': 1.0
# }

# prediction = "void add (int a ,int b ) {\n return a + b;}"
# reference = "void sum ( int first , int second ) {\n return second + first;}"
# result = calc_codebleu([reference], [prediction], lang="c", weights=(0.25, 0.25, 0.25, 0.25), tokenizer=None)
# print(result)

prediction = "fn add ( a , b )->i8 {\n a + b}"
reference = "fn sum ( first , second )->i8 {\n second + first}"
result = calc_codebleu([reference], [prediction], lang="rust", weights=(0.25, 0.25, 0.25, 0.25), tokenizer=None)
print(result)

