(set-logic ALL)
; Constraint ID: dd6e6dd482243547
; Generated at: 2026-04-16 11:31:08
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60064)) (False)
(assert (not (= x 60064)))

; Query: ((== x 60065)) (False)
(assert (not (not (= x 60065))))

(check-sat)
(get-model)
