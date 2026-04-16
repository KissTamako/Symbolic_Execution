(set-logic ALL)
; Frontier Constraint ID: 2b3905e472449a0b
; Generated at: 2026-04-16 14:57:49
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 898)) (False)
(assert (not (not (= x 898))))

(check-sat)
(get-model)
