(set-logic ALL)
; Executed Path ID: 44cd686c52d9e518
; Generated at: 2026-04-17 02:51:35
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const x Int)

; ((== x 2473)) (False)
(assert (not (= x 2473)))
; ((== x 2474)) (False)
(assert (not (= x 2474)))

(check-sat)
(get-model)
