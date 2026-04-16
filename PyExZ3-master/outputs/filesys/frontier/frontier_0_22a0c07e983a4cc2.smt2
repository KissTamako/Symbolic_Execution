(set-logic ALL)
; Constraint ID: 22a0c07e983a4cc2
; Generated at: 2026-04-16 11:52:16
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60511)) (False)
(assert (not (not (= x 60511))))

(check-sat)
(get-model)
