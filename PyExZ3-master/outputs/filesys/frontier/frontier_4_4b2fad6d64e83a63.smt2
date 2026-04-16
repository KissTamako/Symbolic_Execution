(set-logic ALL)
; Frontier Constraint ID: 4b2fad6d64e83a63
; Generated at: 2026-04-16 15:16:56
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1168)) (False)
(assert (not (not (= x 1168))))

(check-sat)
(get-model)
