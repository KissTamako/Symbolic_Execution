(set-logic ALL)
; Executed Path ID: b8b7a991a8e4598f
; Generated at: 2026-04-16 16:03:03
; Solver: Z3Wrapper
; Number of predicates: 6
; Has query: False

(declare-const x Int)

; ((== x 1)) (False)
(assert (not (= x 1)))
; ((== x 3)) (False)
(assert (not (= x 3)))
; ((== x 19)) (False)
(assert (not (= x 19)))
; ((== x 9)) (False)
(assert (not (= x 9)))
; ((== x 12)) (False)
(assert (not (= x 12)))
; ((== x 15)) (True)
(assert (= x 15))

(check-sat)
(get-model)
