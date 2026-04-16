(set-logic ALL)
; Executed Path ID: 37908e8a01be2cb0
; Generated at: 2026-04-16 14:44:34
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const x Int)

; ((== x 748)) (False)
(assert (not (= x 748)))
; ((== x 749)) (False)
(assert (not (= x 749)))

(check-sat)
(get-model)
