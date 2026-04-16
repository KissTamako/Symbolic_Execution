(set-logic ALL)
; Frontier Constraint ID: b5a5dd80074f5ff9
; Generated at: 2026-04-16 15:43:19
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1495)) (False)
(assert (not (not (= x 1495))))

(check-sat)
(get-model)
