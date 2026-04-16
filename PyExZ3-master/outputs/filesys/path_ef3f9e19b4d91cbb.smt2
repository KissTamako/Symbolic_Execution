(set-logic ALL)
; Executed Path ID: ef3f9e19b4d91cbb
; Generated at: 2026-04-16 15:10:06
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const x Int)

; ((== x 1048)) (False)
(assert (not (= x 1048)))
; ((== x 1049)) (False)
(assert (not (= x 1049)))

(check-sat)
(get-model)
