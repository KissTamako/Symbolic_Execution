(set-logic ALL)
; Executed Path ID: 2aca8ae97f7c1925
; Generated at: 2026-04-17 03:12:42
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const x Int)
(declare-const y Int)

; (x) (False)
(assert (not x))
; (y) (True)
(assert y)

(check-sat)
(get-model)
