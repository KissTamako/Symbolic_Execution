(set-logic ALL)
; Executed Path ID: 64440441ddc18f7d
; Generated at: 2026-04-16 16:02:51
; Solver: Z3Wrapper
; Number of predicates: 3
; Has query: False

(declare-const x Int)
(declare-const y Int)
(declare-const z Int)

; (x) (True)
(assert x)
; (y) (True)
(assert y)
; (z) (True)
(assert z)

(check-sat)
(get-model)
