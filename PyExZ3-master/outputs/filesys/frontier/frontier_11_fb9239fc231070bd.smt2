(set-logic ALL)
; Constraint ID: fb9239fc231070bd
; Generated at: 2026-04-16 11:28:21
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59926)) (False)
(assert (not (= x 59926)))

; Query: ((== x 59927)) (False)
(assert (not (not (= x 59927))))

(check-sat)
(get-model)
