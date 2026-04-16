(set-logic ALL)
; Frontier Constraint ID: 1579ea1b2e7d89cf
; Generated at: 2026-04-16 14:41:51
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 490)) (False)
(assert (not (not (= x 490))))

(check-sat)
(get-model)
