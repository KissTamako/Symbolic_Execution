(set-logic ALL)
; Frontier Constraint ID: fff3646b705eb9b4
; Generated at: 2026-04-17 02:53:43
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2542)) (False)
(assert (not (= x 2542)))

; Query: ((== x 2543)) (False)
(assert (not (not (= x 2543))))

(check-sat)
(get-model)
