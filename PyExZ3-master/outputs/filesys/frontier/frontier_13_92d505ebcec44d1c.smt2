(set-logic ALL)
; Frontier Constraint ID: 92d505ebcec44d1c
; Generated at: 2026-04-16 14:36:25
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 355)) (False)
(assert (not (= x 355)))

; Query: ((== x 356)) (False)
(assert (not (not (= x 356))))

(check-sat)
(get-model)
