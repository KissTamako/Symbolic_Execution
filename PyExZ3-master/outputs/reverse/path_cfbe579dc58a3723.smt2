(set-logic ALL)
; Executed Path ID: cfbe579dc58a3723
; Generated at: 2026-04-16 16:03:03
; Solver: Z3Wrapper
; Number of predicates: 1
; Has query: False

(declare-const x Int)

; ((== (- x 5) 0)) (True)
(assert (= (- x 5) 0))

(check-sat)
(get-model)
