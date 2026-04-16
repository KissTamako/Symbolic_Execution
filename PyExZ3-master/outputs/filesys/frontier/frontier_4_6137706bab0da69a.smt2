(set-logic ALL)
; Frontier Constraint ID: 6137706bab0da69a
; Generated at: 2026-04-16 14:41:51
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 493)) (False)
(assert (not (not (= x 493))))

(check-sat)
(get-model)
