(set-logic ALL)
; Executed Path ID: bfa2b4d35eb49f53
; Generated at: 2026-04-17 03:12:55
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: False

(declare-const x Int)

; ((> (* x x) 0)) (True)
(assert (> (* x x) 0))

(check-sat)
(get-model)
