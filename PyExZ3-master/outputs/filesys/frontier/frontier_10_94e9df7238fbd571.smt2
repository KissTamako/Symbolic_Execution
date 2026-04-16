(set-logic ALL)
; Frontier Constraint ID: 94e9df7238fbd571
; Generated at: 2026-04-16 14:57:49
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 877)) (False)
(assert (not (not (= x 877))))

(check-sat)
(get-model)
