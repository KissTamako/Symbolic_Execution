(set-logic ALL)
; Frontier Constraint ID: 4b4c75c606e5bbd4
; Generated at: 2026-04-17 02:51:35
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 2461)) (False)
(assert (not (= x 2461)))

; Query: ((== x 2462)) (False)
(assert (not (not (= x 2462))))

(check-sat)
(get-model)
