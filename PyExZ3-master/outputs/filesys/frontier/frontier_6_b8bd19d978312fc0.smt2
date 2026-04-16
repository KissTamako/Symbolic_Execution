(set-logic ALL)
; Frontier Constraint ID: b8bd19d978312fc0
; Generated at: 2026-04-16 14:40:10
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 421)) (False)
(assert (not (not (= x 421))))

(check-sat)
(get-model)
