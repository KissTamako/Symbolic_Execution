(set-logic ALL)
; Constraint ID: 59a315f82514cd75
; Generated at: 2026-04-16 11:31:08
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60070)) (False)
(assert (not (= x 60070)))

; Query: ((== x 60071)) (False)
(assert (not (not (= x 60071))))

(check-sat)
(get-model)
