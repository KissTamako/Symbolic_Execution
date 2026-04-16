(set-logic ALL)
; Frontier Constraint ID: 64c43f4890a1b6ca
; Generated at: 2026-04-16 14:42:45
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: True

(declare-const x Int)

; ((== x 589)) (False)
(assert (not (= x 589)))

; Query: ((== x 590)) (False)
(assert (not (not (= x 590))))

(check-sat)
(get-model)
