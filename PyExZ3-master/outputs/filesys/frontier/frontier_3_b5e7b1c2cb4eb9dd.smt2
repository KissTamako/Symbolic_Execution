(set-logic ALL)
; Frontier Constraint ID: b5e7b1c2cb4eb9dd
; Generated at: 2026-04-16 14:42:45
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 565)) (False)
(assert (not (= x 565)))

; Query: ((== x 566)) (False)
(assert (not (not (= x 566))))

(check-sat)
(get-model)
