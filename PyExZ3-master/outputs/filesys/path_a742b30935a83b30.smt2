(set-logic ALL)
; Executed Path ID: a742b30935a83b30
; Generated at: 2026-04-16 15:43:19
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const x Int)

; ((== x 1498)) (False)
(assert (not (= x 1498)))
; ((== x 1499)) (False)
(assert (not (= x 1499)))

(check-sat)
(get-model)
