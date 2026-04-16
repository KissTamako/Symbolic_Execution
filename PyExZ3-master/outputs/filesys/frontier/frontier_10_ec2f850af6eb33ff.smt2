(set-logic ALL)
; Constraint ID: ec2f850af6eb33ff
; Generated at: 2026-04-16 11:40:22
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60151)) (False)
(assert (not (not (= x 60151))))

(check-sat)
(get-model)
