(set-logic ALL)
; Constraint ID: cb08a11d0783ae4e
; Generated at: 2026-04-16 04:18:59
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 59314)) (False)
(assert (not (not (= x 59314))))

(check-sat)
(get-model)
