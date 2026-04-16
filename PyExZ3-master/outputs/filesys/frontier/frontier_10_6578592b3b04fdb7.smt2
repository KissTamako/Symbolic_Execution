(set-logic ALL)
; Frontier Constraint ID: 6578592b3b04fdb7
; Generated at: 2026-04-17 02:51:35
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2452)) (False)
(assert (not (not (= x 2452))))

(check-sat)
(get-model)
