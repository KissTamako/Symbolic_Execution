(set-logic ALL)
; Executed Path ID: 67fea2147c22c07b
; Generated at: 2026-04-17 03:12:52
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: False

(declare-const a Int)

; ((== a 2)) (True)
(assert (= a 2))

(check-sat)
(get-model)
