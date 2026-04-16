(set-logic ALL)
; Constraint ID: d389825f655d48a6
; Generated at: 2026-04-16 11:47:24
; Solver: Z3Wrapper
; Number of assertions: 0
; Has query: True

(declare-const se Int)
(declare-const x Int)


; Query: ((== x 60364)) (False)
(assert (not (not (= x 60364))))

(check-sat)
(get-model)
