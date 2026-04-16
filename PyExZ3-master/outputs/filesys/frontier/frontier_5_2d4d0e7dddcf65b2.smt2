(set-logic ALL)
; Frontier Constraint ID: 2d4d0e7dddcf65b2
; Generated at: 2026-04-16 15:56:50
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 1618)) (False)
(assert (not (= x 1618)))

; Query: ((== x 1619)) (False)
(assert (not (not (= x 1619))))

(check-sat)
(get-model)
