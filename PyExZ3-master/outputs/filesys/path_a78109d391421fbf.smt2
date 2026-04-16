(set-logic ALL)
; Executed Path ID: a78109d391421fbf
; Generated at: 2026-04-17 01:52:09
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const x Int)

; ((== x 1873)) (False)
(assert (not (= x 1873)))
; ((== x 1874)) (False)
(assert (not (= x 1874)))

(check-sat)
(get-model)
