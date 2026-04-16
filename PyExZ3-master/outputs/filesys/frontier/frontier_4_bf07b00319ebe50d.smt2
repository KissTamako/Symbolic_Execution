(set-logic ALL)
; Constraint ID: bf07b00319ebe50d
; Generated at: 2026-04-16 11:00:46
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59617)) (False)
(assert (not (not (= x 59617))))

(check-sat)
(get-model)
