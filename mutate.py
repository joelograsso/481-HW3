# This "Starter Code" for EECS 481 HW3 shows how to use a visitor
# pattern to replace nodes in an abstract syntax tree.
#
# Note well:
# (1) It does not show you how to read input from a file.
# (2) It does not show you how to write your resulting source
#       code to a file.
# (3) It does not show you how to "count up" how many of
#       instances of various node types exist.
# (4) It does not show you how to use random numbers.
# (5) It does not show you how to only apply a transformation
#       "once" or "some of the time" based on a condition.
# (6) It does not show you how to copy the AST so that each
#       mutant starts from scratch.
# (7) It does show you how to execute modified code, which is
#       not relevant for this assignment.
#
# ... and so on. It's starter code, not finished code. :-)
#
# But it does highlight how to "check" if a node has a particular type,
# and how to "change" a node to be different.

import ast
import astor
import random
import sys
import copy

class MyVisitor(ast.NodeTransformer):
    """Notes all Numbers and all Strings. Replaces all numbers with 481 and
    strings with 'SE'."""
    def __init__(self, seed):
        random.seed(seed)
        self.numMut = 0
        self.mutLimit = random.randint(1, 5)
        self.randCom = random.randint(10, 25)
        self.randBin = random.randint(10, 25)
        self.randAss = random.randint(75, 100)


    # for each file, different numMut for comp,binop,assign
    def visit_Compare(self, node):
        for i in range(0, len(node.ops)):
            # mutate = random.randint(0,420)
            r1 = random.randint(0, self.randCom)
            r2 = random.randint(0, self.randCom)
            if r1 == r2 and self.numMut < self.mutLimit:
                self.numMut = self.numMut + 1
                comp = random.choice([ast.Eq(), ast.NotEq(), ast.Lt(), ast.LtE(), ast.Gt(), ast.GtE(), ast.Is(), ast.IsNot()])
                node.ops[i] = comp
        node.left = self.visit(node.left)
        for i in range(0, len(node.comparators)):
            node.comparators[i] = self.visit(node.comparators[i])
        return node

    def visit_BinOp(self, node):
        # mutate = random.randint(0,6969)
        r1 = random.randint(0, self.randBin)
        r2 = random.randint(0, self.randBin)
        if r1 == r2 and self.numMut < self.mutLimit:
            self.numMut = self.numMut + 1
            op = random.choice([ast.Add(), ast.Sub(), ast.Mult(), ast.Div(), ast.FloorDiv(), ast.Mod()])
            node.op = op

        node.left = self.visit(node.left)
        node.right = self.visit(node.right)
        return node

    # def visit_BoolOp(self, node):
    #     r1 = random.randint(0, self.randBool)
    #     r2 = random.randint(0, self.randBool)
    #     if r1 == r2 and self.numMut < self.mutLimit:
    #         if isinstance(node.op, ast.And):
    #             node.op = ast.Or()
    #         elif isinstance(node.op, ast.Or):
    #             node.op = ast.And()

    #     for i in range(0, len(node.values)):
    #         node.values[i] = self.visit(node.values[i])
    #     return node

    def visit_Assign(self, node):
        # mutate = random.randint(0,42069)
        r1 = random.randint(0, self.randAss)
        r2 = random.randint(0, self.randAss)
        if r1 == r2 and self.numMut < self.mutLimit:
            self.numMut = self.numMut + 1
            if isinstance(node.value, ast.Num):
                node.value = ast.Num(n=0)
            elif isinstance(node.value, ast.Str):
                node.value = ast.Str(s="")
            elif isinstance(node.value, ast.Call):
                # node.value = node.targets[0]
                node.value = ast.NameConstant(None)
            elif isinstance(node.value, ast.List):
                node.value = ast.List(elts=[], ctx=ast.Store())
            elif isinstance(node.value, ast.Tuple):
                node.value = ast.Tuple(elts=[], ctx=ast.Store())
            elif isinstance(node.value, ast.Set):
                node.value = ast.List(elts=[], ctx=ast.Store())
            elif isinstance(node.value, ast.Dict):
                node.value = ast.Dict(keys=[], values=[])
            elif isinstance(node.value, ast.NameConstant):
                node.value = ast.NameConstant(False)
        return node

# Instead of reading from a file, the starter code always processes in
# a small Python expression literally written in this string below:
#source <_ast.Module object at 0x7f3ff80707b8>
#inputTree <_ast.Module object at 0x7f3feadb0f98>
def main():
    subject = sys.argv[1]
    # subject = "avl.py"
    num = int(sys.argv[2])
    # num = 10
    source = ""
    with open(subject, 'r') as f:
        source = ast.parse(f.read())


    for i in range(0, num):
        visitor = MyVisitor(i)
        inputTree = copy.deepcopy(source)
        outputTree = visitor.visit(inputTree)
        ast.fix_missing_locations(outputTree)
        outputFileName = str(i) + ".py"
        with open(outputFileName, 'w') as output:
            output.write(astor.to_source(outputTree))
    return

if __name__ == "__main__":
    main()

# visitor = MyVisitor().visit(tree)
# print(visitor)




# code = """print(111 + len("hello") + 222 + len("goodbye") < 420 + len("nice") + 6969 + len("cock"))"""
# code = """(1 < a < 10) == (3 != 7) + (4 <= 66) is not (66 is 66)"""
# code = """x = {1,2,3}"""
# # As a sanity check, we'll make sure we're reading the code
# # correctly before we do any processing.
# print("Before any AST transformation")
# print("Code is: ", code)
# print("Code's output is:")
# # exec(code)      # not needed for HW3
# print()
# # v1 = MyVisitor()
# # while dont have enought output files:
# #     out = v1.visit(tree)
# #     write out to file

# # Now we will apply our transformation.
# print("Applying AST transformation")
# tree = ast.parse(code)
# tree = MyVisitor().visit(tree)
# new_tree = astor.dump_tree(tree)
# # print(new_tree)
# # Add lineno & col_offset to the nodes we created
# ast.fix_missing_locations(tree)
# print("Transformed code is: ", astor.to_source(tree))
# co = compile(tree, "", "exec")
# print("Transformed code's output is:")
# exec(co)        # not needed for HW3