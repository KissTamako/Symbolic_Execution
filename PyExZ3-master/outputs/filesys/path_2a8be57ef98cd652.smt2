(set-logic ALL)
; Executed Path ID: 2a8be57ef98cd652
; Generated at: 2026-04-16 14:36:25
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const x Int)

; ((== x 373)) (False)
(assert (not (= x 373)))
; ((== x 374)) (False)
(assert (not (= x 374)))

(check-sat)
(get-model)
