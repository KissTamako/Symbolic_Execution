(set-logic ALL)
; Constraint ID: c1e2c11a6c6a32ee
; Generated at: 2026-04-16 11:14:00
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59854)) (False)
(assert (not (= x 59854)))

; Query: ((== x 59855)) (False)
(assert (not (not (= x 59855))))

(check-sat)
(get-model)
