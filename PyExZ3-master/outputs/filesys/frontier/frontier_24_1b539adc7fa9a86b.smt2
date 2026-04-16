(set-logic ALL)
; Constraint ID: 1b539adc7fa9a86b
; Generated at: 2026-04-16 11:31:08
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60097)) (False)
(assert (not (not (= x 60097))))

(check-sat)
(get-model)
