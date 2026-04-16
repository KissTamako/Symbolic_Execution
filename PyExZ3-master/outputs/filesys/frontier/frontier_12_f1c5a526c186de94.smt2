(set-logic ALL)
; Frontier Constraint ID: f1c5a526c186de94
; Generated at: 2026-04-16 14:57:49
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 880)) (False)
(assert (not (not (= x 880))))

(check-sat)
(get-model)
