(set-logic ALL)
; Frontier Constraint ID: eda97770629f1e73
; Generated at: 2026-04-16 15:10:06
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 1015)) (False)
(assert (not (not (= x 1015))))

(check-sat)
(get-model)
