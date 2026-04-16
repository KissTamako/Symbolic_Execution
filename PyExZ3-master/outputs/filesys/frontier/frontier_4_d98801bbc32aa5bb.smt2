(set-logic ALL)
; Constraint ID: d98801bbc32aa5bb
; Generated at: 2026-04-16 12:01:24
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60667)) (False)
(assert (not (not (= x 60667))))

(check-sat)
(get-model)
