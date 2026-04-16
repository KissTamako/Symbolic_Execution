(set-logic ALL)
; Constraint ID: 135b707f5d33f5f8
; Generated at: 2026-04-16 11:47:24
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60361)) (False)
(assert (not (= x 60361)))

; Query: ((== x 60362)) (False)
(assert (not (not (= x 60362))))

(check-sat)
(get-model)
