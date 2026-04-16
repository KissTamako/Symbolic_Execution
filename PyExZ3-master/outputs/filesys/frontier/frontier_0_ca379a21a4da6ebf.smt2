(set-logic ALL)
; Frontier Constraint ID: ca379a21a4da6ebf
; Generated at: 2026-04-16 16:02:53
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1687)) (False)
(assert (not (not (= x 1687))))

(check-sat)
(get-model)
