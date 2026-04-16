(set-logic ALL)
; Constraint ID: 172538449e0c7777
; Generated at: 2026-04-16 11:29:08
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60010)) (False)
(assert (not (= x 60010)))

; Query: ((== x 60011)) (False)
(assert (not (not (= x 60011))))

(check-sat)
(get-model)
