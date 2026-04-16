(set-logic ALL)
; Frontier Constraint ID: c016e0558246778c
; Generated at: 2026-04-16 14:42:45
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 580)) (False)
(assert (not (= x 580)))

; Query: ((== x 581)) (False)
(assert (not (not (= x 581))))

(check-sat)
(get-model)
