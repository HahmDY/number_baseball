import itertools
import random
import copy

# Use sets for faster operations
permutations = itertools.permutations(range(10), 4)
ans_space = {''.join(map(str, p)) for p in permutations}
result_space = {(0,0),(0,1),(0,2),(0,3),(0,4),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(2,2),(3,0),(3,1), (4,0)}

def match(ans, query, score):
    s, b = 0, 0
    for i in range(4):
        if ans[i] == query[i]:
            s += 1
        elif ans[i] in query:
            b += 1
    return s == score[0] and b == score[1]

def get_ans_space(ans_space, history):
    ans_space_copy = ans_space.copy()
    for query, score in history.items():
        ans_space_copy = {ans for ans in ans_space_copy if match(ans, query, score)}
    return ans_space_copy

def select_query(ans_space, history):
    score = {}
    original_ans_space = ans_space.copy()
    query_space = original_ans_space - set(history.keys())
    print(query_space)
    for query in query_space:
        score[query] = 0
        for result in result_space:
            psuedo_history = history.copy()
            psuedo_history[query] = result
            reduced_ans_space = get_ans_space(original_ans_space, psuedo_history)
            score[query] += len(original_ans_space) - len(reduced_ans_space)
    return max(score, key=score.get)

strike = 0
ball = 0
history = {}
step = 1

while strike != 4:
    # select query
    print("selecting query", step)
    if step == 1:
        first_query = random.sample(range(10), 4)
        query = ''.join(map(str, first_query))
    elif step == 2:
        remaining_numbers = [num for num in range(10) if num not in first_query]
        second_query = random.sample(remaining_numbers, 4)
        query = ''.join(map(str, second_query))
    else:
        query = select_query(ans_space, history)

    # get result
    print("get result", step) 
    print('query: ', query)
    strike = int(input('strike: '))
    ball = int(input('ball: '))
    history[query] = [strike, ball]
    
    #update ans_space
    print("updating ans_space", step)
    ans_space = get_ans_space(ans_space, history)
    step += 1
    
    # game over
    if strike == 4:
        print("The answer is...!!!!!!!: ", query)
        print(f"Guessed correctly in {step} tries!")
        break
    