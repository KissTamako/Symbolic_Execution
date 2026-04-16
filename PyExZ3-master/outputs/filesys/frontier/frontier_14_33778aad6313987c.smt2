(set-logic ALL)
; Frontier Constraint ID: 33778aad6313987c
; Generated at: 2026-04-17 02:53:43
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2533)) (False)
(assert (not (not (= x 2533))))

(check-sat)
(get-model)
