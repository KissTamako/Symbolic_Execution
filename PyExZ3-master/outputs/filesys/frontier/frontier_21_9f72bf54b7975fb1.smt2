(set-logic ALL)
; Frontier Constraint ID: 9f72bf54b7975fb1
; Generated at: 2026-04-16 14:42:45
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 592)) (False)
(assert (not (= x 592)))

; Query: ((== x 593)) (False)
(assert (not (not (= x 593))))

(check-sat)
(get-model)
