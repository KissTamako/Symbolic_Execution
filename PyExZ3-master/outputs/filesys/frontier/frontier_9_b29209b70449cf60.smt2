(set-logic ALL)
; Constraint ID: b29209b70449cf60
; Generated at: 2026-04-16 11:28:21
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59923)) (False)
(assert (not (= x 59923)))

; Query: ((== x 59924)) (False)
(assert (not (not (= x 59924))))

(check-sat)
(get-model)
