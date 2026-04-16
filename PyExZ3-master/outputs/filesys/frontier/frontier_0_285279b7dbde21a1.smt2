(set-logic ALL)
; Frontier Constraint ID: 285279b7dbde21a1
; Generated at: 2026-04-17 02:53:43
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2512)) (False)
(assert (not (not (= x 2512))))

(check-sat)
(get-model)
