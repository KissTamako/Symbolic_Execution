(set-logic ALL)
; Executed Path ID: 411844fe6b3d5534
; Generated at: 2026-04-17 03:12:47
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const x Int)

; ((== x 2848)) (False)
(assert (not (= x 2848)))
; ((== x 2849)) (False)
(assert (not (= x 2849)))

(check-sat)
(get-model)
