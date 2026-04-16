(set-logic ALL)
; Executed Path ID: 0f322b951a8a03ef
; Generated at: 2026-04-16 14:41:51
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const x Int)

; ((== x 523)) (False)
(assert (not (= x 523)))
; ((== x 524)) (False)
(assert (not (= x 524)))

(check-sat)
(get-model)
