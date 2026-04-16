(set-logic ALL)
; Constraint ID: 067a3ce56eea3f25
; Generated at: 2026-04-16 11:52:16
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60514)) (False)
(assert (not (= x 60514)))

; Query: ((== x 60515)) (False)
(assert (not (not (= x 60515))))

(check-sat)
(get-model)
