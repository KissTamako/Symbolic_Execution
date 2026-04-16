(set-logic ALL)
; Constraint ID: 24ef30e45cc508c4
; Generated at: 2026-04-16 11:31:08
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60085)) (False)
(assert (not (= x 60085)))

; Query: ((== x 60086)) (False)
(assert (not (not (= x 60086))))

(check-sat)
(get-model)
