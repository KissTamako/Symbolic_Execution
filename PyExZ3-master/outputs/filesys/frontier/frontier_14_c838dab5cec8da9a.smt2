(set-logic ALL)
; Frontier Constraint ID: c838dab5cec8da9a
; Generated at: 2026-04-16 14:57:49
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 883)) (False)
(assert (not (not (= x 883))))

(check-sat)
(get-model)
