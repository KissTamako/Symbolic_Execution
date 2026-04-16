(set-logic ALL)
; Frontier Constraint ID: 46b0588ebdf2662c
; Generated at: 2026-04-16 15:56:50
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1630)) (False)
(assert (not (= x 1630)))

; Query: ((== x 1631)) (False)
(assert (not (not (= x 1631))))

(check-sat)
(get-model)
