(set-logic ALL)
; Executed Path ID: b9bffa4338865de7
; Generated at: 2026-04-16 14:57:49
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const x Int)

; ((== x 898)) (False)
(assert (not (= x 898)))
; ((== x 899)) (False)
(assert (not (= x 899)))

(check-sat)
(get-model)
