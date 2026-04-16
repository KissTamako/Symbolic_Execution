(set-logic ALL)
; Constraint ID: 21e18c038e04c834
; Generated at: 2026-04-16 04:51:40
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59386)) (False)
(assert (not (= x 59386)))

; Query: ((== x 59387)) (False)
(assert (not (not (= x 59387))))

(check-sat)
(get-model)
