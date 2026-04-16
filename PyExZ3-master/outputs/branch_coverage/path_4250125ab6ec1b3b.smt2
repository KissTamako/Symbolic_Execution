(set-logic ALL)
; Executed Path ID: 4250125ab6ec1b3b
; Generated at: 2026-04-17 03:12:44
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const x Int)
(declare-const y Int)

; ((> x 0)) (True)
(assert (> x 0))
; ((> y 0)) (True)
(assert (> y 0))

(check-sat)
(get-model)
