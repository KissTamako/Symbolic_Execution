(set-logic ALL)
; Executed Path ID: 82321ad6459b78fa
; Generated at: 2026-04-16 15:26:57
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const x Int)

; ((== x 1348)) (False)
(assert (not (= x 1348)))
; ((== x 1349)) (False)
(assert (not (= x 1349)))

(check-sat)
(get-model)
