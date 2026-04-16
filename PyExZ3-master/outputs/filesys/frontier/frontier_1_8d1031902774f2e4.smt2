(set-logic ALL)
; Constraint ID: 8d1031902774f2e4
; Generated at: 2026-04-16 10:45:36
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59536)) (False)
(assert (not (= x 59536)))

; Query: ((== x 59537)) (False)
(assert (not (not (= x 59537))))

(check-sat)
(get-model)
