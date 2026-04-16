(set-logic ALL)
; Path ID: a18e5f1efb4b735f
; Generated at: 2026-04-16 11:31:08
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60061)) (False)
(assert (not (not (= x 60061))))

(check-sat)
(get-model)
