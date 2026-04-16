(set-logic ALL)
; Frontier Constraint ID: 49f7dcd70ef5668f
; Generated at: 2026-04-16 14:43:36
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 658)) (False)
(assert (not (= x 658)))

; Query: ((== x 659)) (False)
(assert (not (not (= x 659))))

(check-sat)
(get-model)
