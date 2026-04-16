(set-logic ALL)
; Executed Path ID: f830ba684a9f9e40
; Generated at: 2026-04-16 15:56:50
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const x Int)

; ((== x 1648)) (False)
(assert (not (= x 1648)))
; ((== x 1649)) (False)
(assert (not (= x 1649)))

(check-sat)
(get-model)
