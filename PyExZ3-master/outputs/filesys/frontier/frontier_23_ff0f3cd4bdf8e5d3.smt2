(set-logic ALL)
; Constraint ID: ff0f3cd4bdf8e5d3
; Generated at: 2026-04-16 11:52:16
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60544)) (False)
(assert (not (= x 60544)))

; Query: ((== x 60545)) (False)
(assert (not (not (= x 60545))))

(check-sat)
(get-model)
