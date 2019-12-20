#!/usr/bin/env python3
import ast
import re
import warnings

import astor

class WireCollector(ast.NodeTransformer):
    def __init__(self):
        self.wire_stmts = []
    def visit_Expr(self, expr_stmt: ast.Expr):
        expr = expr_stmt.value
        if isinstance(expr,  ast.Compare):
            #Maybe should only fix expression with 1 comparator but
            #this has the side-effect of fixing buggy code so why not?
            if isinstance(expr.ops[0], ast.LtE):
                # Can't extract the col_offset of the LtE directly so
                # record the start of the expr and the offset of the
                # first comparator.  The last '<=' in this range must
                # be the LtE we want.
                # This necessary because of stuff like:
                #   bv[x <= y] <= r <= s
                #              ^
                # is the char of interest
                if len(expr.comparators) != 1:
                    warnings.warn(
                        f'`{astor.to_source(expr_stmt)[:-1]}` is a compound comparison.  '
                        f'Will assume that {astor.to_source(expr.left)[:-1]} is the intended wire target.  '
                         'This was almost certainly a bug, but if you knew what you were doing this just broke your code.'
                    )
                self.wire_stmts.append((
                    # -1 because for some reason this is 1 indexed. smh.
                    expr.lineno - 1,
                    expr.col_offset,
                    expr.comparators[0].col_offset))

wire_re = re.compile(r'.+(\<\=)\s*')
new_wire_re = re.compile(r'.+(\@\=)\s*')
def rewrite_wires(src_txt):
    src_ast = ast.parse(src_txt)
    wire_collector = WireCollector()
    wire_collector.visit(src_ast)
    src_lines = src_txt.split('\n')
    for lineno, expr_offset, end_offset in wire_collector.wire_stmts:
        src_line = src_lines[lineno]
        fragment = src_line[expr_offset : end_offset]
        match = wire_re.match(fragment)
        assert match, (lineno, expr_offset, end_offset, src_line, fragment)
        # get the span of the LtE
        span = match.span(1)
        assert fragment[slice(*span)] == '<='
        assert src_line[expr_offset + span[0]] == '<'
        new_fragment = ''.join((fragment[:span[0]], '@', fragment[span[0] + 1:]))
        assert len(new_fragment) == len(fragment)
        new_match = new_wire_re.match(new_fragment)
        assert new_match
        assert new_match.span(1) == span
        # Would be slighter faster to construct the new_src_line directly
        # instead of constructing the new_fragment then the new_src_line.
        # But I want to have to the assertions.  Also I doubt
        # Performance will ever be an issue
        new_src_line = ''.join((
            src_line[:expr_offset],
            new_fragment,
            src_line[end_offset:]))
        assert len(new_src_line) == len(src_line)
        src_lines[lineno] = new_src_line

    new_src_txt = '\n'.join(src_lines)
    assert len(src_txt) == len(new_src_txt)
    return new_src_txt

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        raise RuntimeError(f'Usage: {sys.argv[0]} <src_file> <dst_file>')
    with open(sys.argv[1], 'r') as f:
        src_txt = f.read()

    try:
        ast.parse(src_txt)
    except SyntaxError:
        raise RuntimeError(f'{sys.argv[1]} is not a valid python file') from None

    new_src_txt= rewrite_wires(src_txt)

    # Make sure we still have have valid python
    try:
        ast.parse(new_src_txt)
    except SyntaxError:
        raise RuntimeError(f'Rewrite resulted in invalid python') from None

    with open(sys.argv[2], 'w') as f:
        f.write(new_src_txt)
