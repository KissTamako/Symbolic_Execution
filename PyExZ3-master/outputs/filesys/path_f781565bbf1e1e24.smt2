(set-logic ALL)
; Executed Path ID: f781565bbf1e1e24
; Generated at: 2026-04-16 16:02:53
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const x Int)

; ((== x 1723)) (False)
(assert (not (= x 1723)))
; ((== x 1724)) (False)
(assert (not (= x 1724)))

(check-sat)
(get-model)
