(set-logic ALL)
; Constraint ID: 68246f0b4e09670f
; Generated at: 2026-04-16 11:31:08
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60091)) (False)
(assert (not (not (= x 60091))))

(check-sat)
(get-model)
