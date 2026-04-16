(set-logic ALL)
; Frontier Constraint ID: 1fe61c52916d8842
; Generated at: 2026-04-17 02:53:43
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2545)) (False)
(assert (not (not (= x 2545))))

(check-sat)
(get-model)
