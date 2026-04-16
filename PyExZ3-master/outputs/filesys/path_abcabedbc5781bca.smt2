(set-logic ALL)
; Executed Path ID: abcabedbc5781bca
; Generated at: 2026-04-16 15:16:56
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const x Int)

; ((== x 1198)) (False)
(assert (not (= x 1198)))
; ((== x 1199)) (False)
(assert (not (= x 1199)))

(check-sat)
(get-model)
