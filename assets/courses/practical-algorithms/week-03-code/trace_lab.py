"""Trace the actual solution on a small input; Python standard library only.
Run: python trace_lab.py --case FUNCTION
Use --student after implementing student_week_03.py.
The state printed before line N is the result of earlier executed lines.
추적 행은 실행 직전의 상태입니다. 표시된 행이 실행되기 전 값을 읽으세요.
Tracing and displaying containers add overhead; exclude them from algorithm costs.
"""
import argparse
from collections import deque
import inspect
import linecache
import sys
import solutions
from structures import linked, linked_values
CASES = {'search_matrix': ('([[1, 3, 5], [7, 9, 11]], 9)', True), 'search_rotated': ('([4, 5, 6, 7, 0, 1, 2], 0)', 4), 'reverse_list': ('(linked([2, 5, 8]),)', [8, 5, 2]), 'merge_lists': ('(linked([1, 3]), linked([2, 4]))', [1, 2, 3, 4])}

def display(value, depth=0):
    if depth > 4:
        return "..."
    if hasattr(value, 'next') and hasattr(value, 'val'):
        values, seen = [], set()
        while value is not None and len(values) < 12:
            if id(value) in seen:
                values.append('cycle'); break
            seen.add(id(value)); values.append(value.val); value = value.next
        return {'chain': values, 'continues': value is not None}
    if hasattr(value, 'left') and hasattr(value, 'val'):
        return {'node': value.val, 'left': getattr(value.left, 'val', None),
                'right': getattr(value.right, 'val', None)}
    if isinstance(value, dict):
        return {str(k): display(v, depth+1) for k,v in list(value.items())[:12]}
    if isinstance(value, (list, tuple, deque)):
        return [display(v, depth+1) for v in list(value)[:12]]
    if isinstance(value, set):
        return sorted(value, key=repr)
    if hasattr(value, '__dict__'):
        return display(vars(value), depth+1)
    return value

def run_case(name, student=False, trace=True):
    module = __import__('student_week_03') if student else solutions
    source_path = inspect.getsourcefile(module)
    def observe(frame, event, arg):
        if frame.f_code.co_filename == source_path:
            state = {k: display(v) for k,v in frame.f_locals.items()
                     if not callable(v) and not k.startswith('__')}
            if event == 'line':
                code = linecache.getline(source_path, frame.f_lineno).strip()
                print(f"before L{frame.f_lineno} {code} | {state}")
            elif event == 'return':
                print(f"return {frame.f_code.co_name}: {display(arg)}")
        return observe
    args_text, expected = CASES[name]
    args = eval(args_text, globals())  # fixed, local teaching inputs only
    old_trace = sys.gettrace()
    if trace: sys.settrace(observe)
    try:
        if name == 'MinStack':
            stack = module.MinStack()
            for value in [2,1,1]: stack.push(value)
            result = [stack.getMin()]
            stack.pop(); result.append(stack.getMin())
            stack.pop(); result.append(stack.getMin())
        else:
            result = getattr(module, name)(*args)
    finally:
        sys.settrace(old_trace)
    if name in ('reverse_list', 'merge_lists'): result = linked_values(result)
    if name in ('subsets', 'combinations', 'three_sum'):
        assert sorted(map(tuple,result)) == sorted(map(tuple,expected)), (result,expected)
    elif name == 'course_order':
        n, edges = args
        assert sorted(result) == list(range(n))
        positions = {v:i for i,v in enumerate(result)}
        assert all(positions[b] < positions[a] for a,b in edges)
    else:
        assert result == expected, (result, expected)
    print(f"{name}: {display(result)}; example check passed")
    return result

if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', choices=list(CASES))
    parser.add_argument('--student', action='store_true')
    parser.add_argument('--no-trace', action='store_true')
    args=parser.parse_args()
    for name in ([args.case] if args.case else CASES):
        print('\n===', name, '===')
        run_case(name, args.student, not args.no_trace)
