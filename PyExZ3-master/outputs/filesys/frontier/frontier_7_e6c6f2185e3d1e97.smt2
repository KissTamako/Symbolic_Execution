(set-logic ALL)
; Constraint ID: e6c6f2185e3d1e97
; Generated at: 2026-04-16 11:47:24
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60370)) (False)
(assert (not (= x 60370)))

; Query: ((== x 60371)) (False)
(assert (not (not (= x 60371))))

(check-sat)
(get-model)
