(set-logic ALL)
; Executed Path ID: 2b7ebd9e0226c592
; Generated at: 2026-04-17 02:53:43
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const x Int)

; ((== x 2548)) (False)
(assert (not (= x 2548)))
; ((== x 2549)) (False)
(assert (not (= x 2549)))

(check-sat)
(get-model)
