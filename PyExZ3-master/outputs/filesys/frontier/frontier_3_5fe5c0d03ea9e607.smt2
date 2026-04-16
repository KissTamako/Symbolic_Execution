(set-logic ALL)
; Frontier Constraint ID: 5fe5c0d03ea9e607
; Generated at: 2026-04-16 15:26:57
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1315)) (False)
(assert (not (= x 1315)))

; Query: ((== x 1316)) (False)
(assert (not (not (= x 1316))))

(check-sat)
(get-model)
