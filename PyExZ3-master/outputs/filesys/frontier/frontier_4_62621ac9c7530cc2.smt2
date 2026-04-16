(set-logic ALL)
; Constraint ID: 62621ac9c7530cc2
; Generated at: 2026-04-16 11:40:22
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60142)) (False)
(assert (not (not (= x 60142))))

(check-sat)
(get-model)
