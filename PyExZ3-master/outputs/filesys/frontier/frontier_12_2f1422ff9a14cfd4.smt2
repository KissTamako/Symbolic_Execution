(set-logic ALL)
; Frontier Constraint ID: 2f1422ff9a14cfd4
; Generated at: 2026-04-17 03:12:47
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2830)) (False)
(assert (not (not (= x 2830))))

(check-sat)
(get-model)
