(set-logic ALL)
; Constraint ID: d1eb84f35aa13627
; Generated at: 2026-04-16 11:03:34
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59713)) (False)
(assert (not (= x 59713)))

; Query: ((== x 59714)) (False)
(assert (not (not (= x 59714))))

(check-sat)
(get-model)
