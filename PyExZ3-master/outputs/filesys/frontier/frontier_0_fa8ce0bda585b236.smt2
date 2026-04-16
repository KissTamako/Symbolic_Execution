(set-logic ALL)
; Frontier Constraint ID: fa8ce0bda585b236
; Generated at: 2026-04-16 14:42:45
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 562)) (False)
(assert (not (not (= x 562))))

(check-sat)
(get-model)
