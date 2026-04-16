(set-logic ALL)
; Executed Path ID: 2977a13bbece3c4b
; Generated at: 2026-04-16 16:02:50
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const x Int)
(declare-const y Int)

; ((>= y 4294967296)) (True)
(assert (>= y 4294967296))
; ((== x 4294967296)) (False)
(assert (not (= x 4294967296)))

(check-sat)
(get-model)
