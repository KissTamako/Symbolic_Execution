(set-logic ALL)
; Constraint ID: d7a802928acc7d88
; Generated at: 2026-04-16 11:28:21
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59929)) (False)
(assert (not (not (= x 59929))))

(check-sat)
(get-model)
