(set-logic ALL)
; Constraint ID: d355ee8febccf980
; Generated at: 2026-04-16 04:08:23
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59251)) (False)
(assert (not (= x 59251)))

; Query: ((== x 59252)) (False)
(assert (not (not (= x 59252))))

(check-sat)
(get-model)
