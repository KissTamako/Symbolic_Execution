(set-logic ALL)
; Frontier Constraint ID: af90ebc955303553
; Generated at: 2026-04-17 03:12:47
; Solver: Z3Wrapper
; Number of predicates: 0
; Has query: True

(declare-const x Int)


; Query: ((== x 2818)) (False)
(assert (not (not (= x 2818))))

(check-sat)
(get-model)
