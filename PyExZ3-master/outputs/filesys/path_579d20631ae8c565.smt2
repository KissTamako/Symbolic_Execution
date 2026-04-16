(set-logic ALL)
; Executed Path ID: 579d20631ae8c565
; Generated at: 2026-04-16 14:43:36
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const x Int)

; ((== x 673)) (False)
(assert (not (= x 673)))
; ((== x 674)) (False)
(assert (not (= x 674)))

(check-sat)
(get-model)
