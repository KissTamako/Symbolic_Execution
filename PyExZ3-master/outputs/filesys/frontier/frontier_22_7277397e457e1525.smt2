(set-logic ALL)
; Constraint ID: 7277397e457e1525
; Generated at: 2026-04-16 11:49:33
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60469)) (False)
(assert (not (not (= x 60469))))

(check-sat)
(get-model)
