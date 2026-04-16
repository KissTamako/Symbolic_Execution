(set-logic ALL)
; Frontier Constraint ID: 82cf32b32a175fb2
; Generated at: 2026-04-16 14:43:36
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 670)) (False)
(assert (not (not (= x 670))))

(check-sat)
(get-model)
