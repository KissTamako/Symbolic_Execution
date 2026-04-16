(set-logic ALL)
; Frontier Constraint ID: cea11907a9373ed4
; Generated at: 2026-04-17 02:51:35
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2458)) (False)
(assert (not (not (= x 2458))))

(check-sat)
(get-model)
